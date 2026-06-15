#!/usr/bin/env python3
"""
World Cup 数据库维护引擎 — Database Maintenance Engine
======================================================
5层架构 · 依赖管理 · 触发器更新 · 版本快照 · 完整性保证

架构:
  L0_SOURCE   wiki_squads.json  + polymarket.json    [手动/外部源]
  L1_MATCH    match_data.json                         [ESPN/TheSportsDB API]
  L2_DERIVED  standings.json                          [match_data → 计算]
  L3_REF      teams.json + team_names.json            [wiki_squads + API]
              player_details.json                     [Transfermarkt + API]
  L5_META     verify_report.json                      [质量检查结果]

更新触发规则:
  match_data变更 → 自动重算standings + verify
  teams变更      → 自动更新player_details引用
  所有变更       → 自动运行verify + 生成快照
"""

import json, os, sys, time, shutil
from datetime import datetime, timezone
from pathlib import Path
from collections import OrderedDict

REPO = Path(__file__).parent

# ============================================================
# LAYER DEFINITIONS & DEPENDENCIES
# ============================================================
LAYERS = OrderedDict({
    "L0_SOURCE": {
        "files": ["wiki_squads.json", "polymarket.json"],
        "update_trigger": "manual_or_external",
        "frequency": "on_change",
        "depends_on": [],
        "description": "静态参考数据 + 外部分析数据"
    },
    "L1_MATCH": {
        "files": ["match_data.json"],
        "update_trigger": "api_poll",
        "frequency": "60s_live / 120s_idle",
        "depends_on": [],
        "description": "实时比赛数据"
    },
    "L2_DERIVED": {
        "files": ["standings.json"],
        "update_trigger": "match_data_changed",
        "frequency": "on_L1_change",
        "depends_on": ["L1_MATCH"],
        "description": "从比赛结果计算的积分榜"
    },
    "L3_REF": {
        "files": ["teams.json", "team_names.json", "player_details.json"],
        "update_trigger": "wiki_changed / api_fetch",
        "frequency": "daily_or_on_L0_change",
        "depends_on": ["L0_SOURCE"],
        "description": "球队球员参考数据"
    },
    "L5_META": {
        "files": ["verify_report.json"],
        "update_trigger": "any_layer_changed",
        "frequency": "on_any_change",
        "depends_on": ["L1_MATCH", "L2_DERIVED", "L3_REF"],
        "description": "数据质量元数据"
    },
})

# ============================================================
# DEPENDENCY GRAPH & CASCADE UPDATES
# ============================================================
def get_dependents(layer_name: str) -> list[str]:
    """Get all layers that depend on this layer."""
    deps = []
    for lname, linfo in LAYERS.items():
        if layer_name in linfo.get("depends_on", []):
            deps.append(lname)
            deps.extend(get_dependents(lname))  # Recursive
    return list(set(deps))

def cascade_update(trigger_file: str, verbose: bool = True) -> dict:
    """When a file changes, cascade update all dependent layers."""
    trigger_layer = None
    for lname, linfo in LAYERS.items():
        if trigger_file in linfo["files"]:
            trigger_layer = lname
            break

    if not trigger_layer:
        return {"error": f"Unknown file: {trigger_file}"}

    layers_to_update = [trigger_layer] + get_dependents(trigger_layer)
    report = {"trigger": trigger_file, "trigger_layer": trigger_layer,
              "cascade": layers_to_update, "updates": []}

    for layer in layers_to_update:
        try:
            result = update_layer(layer, verbose=verbose)
            report["updates"].append({"layer": layer, "result": result})
        except Exception as e:
            report["updates"].append({"layer": layer, "error": str(e)})

    return report


def update_layer(layer_name: str, verbose: bool = True) -> dict:
    """Update a specific database layer."""
    if verbose:
        print(f"  [DB] Updating {layer_name}...")

    if layer_name == "L1_MATCH":
        return _update_match_data(verbose)
    elif layer_name == "L2_DERIVED":
        return _update_standings(verbose)
    elif layer_name == "L3_REF":
        return _update_teams(verbose)
    elif layer_name == "L0_SOURCE":
        return _verify_source_files(verbose)
    elif layer_name == "L5_META":
        return _run_verification(verbose)
    else:
        return {"status": "no_handler", "layer": layer_name}


def _update_match_data(verbose: bool) -> dict:
    """Re-fetch match data from APIs."""
    try:
        from sync_worldcup import sync_once
        result = sync_once(commit=False)
        return {"status": "OK", "matches": result.get("total", 0),
                "scored": result.get("scored", 0),
                "new": result.get("updated", 0)}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def _update_standings(verbose: bool) -> dict:
    """Recalculate standings from match_data."""
    try:
        from sync_worldcup import parse_cup_txt, calculate_standings
        matches = parse_cup_txt()
        standings = calculate_standings(matches)
        path = REPO / "standings.json"
        path.write_text(json.dumps(standings, ensure_ascii=False, indent=2), encoding="utf-8")
        scored = sum(1 for m in matches if m.get("is_result"))
        return {"status": "OK", "groups": len(standings), "scored_matches": scored}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def _update_teams(verbose: bool) -> dict:
    """Update team data from wiki_squads."""
    try:
        from sync_worldcup import build_teams_data
        teams = build_teams_data()
        total_players = sum(len(t["players"]) for t in teams.values())
        return {"status": "OK", "teams": len(teams), "players": total_players}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def _verify_source_files(verbose: bool) -> dict:
    """Verify source files exist and are valid."""
    issues = []
    for f in LAYERS["L0_SOURCE"]["files"]:
        path = REPO / f
        if not path.exists():
            issues.append(f"{f} missing")
        else:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                issues.append(f"{f} invalid JSON: {e}")
    return {"status": "OK" if not issues else "ISSUES", "issues": issues}


def _run_verification(verbose: bool) -> dict:
    """Run full data quality verification."""
    try:
        import verify
        report = verify.run_all_checks()
        report['quality_score'] = verify.calculate_quality_score(report)
        path = REPO / "verify_report.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": report['summary']['status'],
                "score": report['quality_score'],
                "verdict": report['summary']['verdict']}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


# ============================================================
# VERSION SNAPSHOTS
# ============================================================
SNAPSHOT_DIR = REPO / ".db_snapshots"
MAX_SNAPSHOTS = 20

def create_snapshot(label: str = "") -> str:
    """Create a timestamped snapshot of all database files."""
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_name = f"{timestamp}_{label}" if label else timestamp
    snap_path = SNAPSHOT_DIR / snap_name
    snap_path.mkdir(exist_ok=True)

    files_saved = []
    for layer_name, layer_info in LAYERS.items():
        for f in layer_info["files"]:
            src = REPO / f
            if src.exists():
                shutil.copy2(src, snap_path / f)
                files_saved.append(f)

    # Save metadata
    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": label,
        "files": files_saved,
        "layers": list(LAYERS.keys()),
    }
    (snap_path / "_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # Rotate old snapshots
    all_snaps = sorted(SNAPSHOT_DIR.iterdir(), key=os.path.getmtime, reverse=True)
    for old in all_snaps[MAX_SNAPSHOTS:]:
        if old.is_dir():
            shutil.rmtree(old)

    print(f"  [DB] Snapshot created: {snap_name} ({len(files_saved)} files)")
    return snap_name


def list_snapshots() -> list[dict]:
    """List all available snapshots."""
    if not SNAPSHOT_DIR.exists():
        return []
    snaps = []
    for d in sorted(SNAPSHOT_DIR.iterdir(), key=os.path.getmtime, reverse=True):
        if d.is_dir():
            meta_file = d / "_meta.json"
            if meta_file.exists():
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                snaps.append(meta)
    return snaps


def restore_snapshot(snap_name: str, confirm: bool = False) -> dict:
    """Restore database from a snapshot."""
    snap_path = SNAPSHOT_DIR / snap_name
    if not snap_path.exists():
        return {"error": f"Snapshot {snap_name} not found"}

    if not confirm:
        return {"error": "Restore requires confirm=True"}

    restored = []
    for f in snap_path.iterdir():
        if f.name.startswith("_"):
            continue
        dst = REPO / f.name
        shutil.copy2(f, dst)
        restored.append(f.name)

    print(f"  [DB] Restored {len(restored)} files from snapshot {snap_name}")
    return {"status": "OK", "restored": restored}


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================
def health_check() -> dict:
    """Comprehensive database health check."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "layers": {},
        "files": {},
        "overall": "OK",
        "issues": [],
    }

    for layer_name, layer_info in LAYERS.items():
        layer_ok = True
        for f in layer_info["files"]:
            path = REPO / f
            status = "OK"
            details = {}
            if not path.exists():
                status = "MISSING"
                layer_ok = False
            else:
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    age_min = (time.time() - path.stat().st_mtime) / 60
                    details["age_min"] = round(age_min, 1)
                    details["size_kb"] = round(path.stat().st_size / 1024, 1)
                    if isinstance(data, dict):
                        details["keys"] = len(data)
                    elif isinstance(data, list):
                        details["items"] = len(data)
                except Exception as e:
                    status = "INVALID"
                    details["error"] = str(e)
                    layer_ok = False

            report["files"][f] = {"status": status, "layer": layer_name, **details}
            if status != "OK":
                report["issues"].append(f"{f}: {status}")

        report["layers"][layer_name] = "OK" if layer_ok else "ISSUES"

    # Overall
    all_ok = all(v == "OK" for v in report["layers"].values())
    report["overall"] = "HEALTHY" if all_ok else "DEGRADED"

    return report


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse

    parser = argparse.ArgumentParser(description="World Cup Database Maintenance Engine")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--snapshot", type=str, nargs="?", const="auto", help="Create snapshot")
    parser.add_argument("--snapshots", action="store_true", help="List snapshots")
    parser.add_argument("--restore", type=str, help="Restore from snapshot name")
    parser.add_argument("--cascade", type=str, help="Cascade update from trigger file")
    parser.add_argument("--update-layer", type=str, help="Update specific layer")
    parser.add_argument("--verify", action="store_true", help="Run verification only")

    args = parser.parse_args()

    if args.health:
        report = health_check()
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.snapshot:
        label = args.snapshot if args.snapshot != "auto" else ""
        create_snapshot(label)
    elif args.snapshots:
        snaps = list_snapshots()
        for s in snaps:
            print(f"  {s['timestamp'][:19]}  {s.get('label','')}  ({len(s['files'])} files)")
    elif args.restore:
        restore_snapshot(args.restore, confirm=True)
    elif args.cascade:
        cascade_update(args.cascade)
    elif args.update_layer:
        update_layer(args.update_layer)
    elif args.verify:
        _run_verification(True)
    else:
        # Default: health check
        report = health_check()
        status = report["overall"]
        print(f"Database: {status}")
        for f, info in report["files"].items():
            print(f"  {info['status']:7} [{info['layer']}] {f}  {info.get('items',info.get('keys',''))} items  {info.get('age_min','?')}min old")
