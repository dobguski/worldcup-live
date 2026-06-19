#!/usr/bin/env python3
"""
Operational Database Layer — Publish Pipeline
==============================================
Reads staging data → validates → promotes to production → pushes to GitHub.
Only publishes if validation passes. Decoupled from ingest: runs on its own schedule.
"""
import json, sys, os, time, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

REPO_DIR = Path(__file__).parent
STAGE_DIR = REPO_DIR / '_stage'

# ── Config ──
PUBLISH_INTERVAL = 45  # seconds between publish cycles
MIN_QUALITY_SCORE = 75  # minimum quality score to auto-publish

# ═══════════════════════════════════════════════════════════════
# SYNC ENGINE (moved from sync_worldcup — the core transformation)
# ═══════════════════════════════════════════════════════════════

def merge_and_build():
    """Merge staged API data into cup.txt and build production JSON files.
    Returns dict with status info.
    """
    # Import from main sync module for core logic
    sys.path.insert(0, str(REPO_DIR))
    from sync_worldcup import (
        parse_cup_txt, calculate_standings, merge_api_results,
        update_match_in_file, to_beijing_time, TEAM_CN, team_cn,
        fetch_espn_matches, fetch_thesportsdb_matches, fetch_fifa_matches,
        check_missing_results, normalize_name, CUP_TXT, DATA_JSON, STANDINGS_JSON,
        TEAM_NAMES_JSON, TEAMS_JSON, git_commit_and_push, bump_counter,
    )

    result = {'updated': 0, 'published': False, 'errors': []}

    try:
        # 1. Fetch APIs
        espn = fetch_espn_matches()
        tsdb = fetch_thesportsdb_matches()
        fifa = fetch_fifa_matches()
        all_api = espn + tsdb + fifa
        print(f'  [PUB] ESPN:{len(espn)} TSDB:{len(tsdb)} FIFA:{len(fifa)}')

        # 2. Parse cup.txt
        matches = parse_cup_txt()
        scored = sum(1 for m in matches if m.get('is_result'))
        print(f'  [PUB] {scored}/{len(matches)} matches have results')

        # 3. Merge new results
        updated = merge_api_results(matches, all_api)
        new_results = []
        if updated:
            for m in updated:
                update_match_in_file(m, m['home_score'], m['away_score'])
                new_results.append(f"{m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']}")
            print(f'  [PUB] {len(updated)} new result(s)')
        else:
            print(f'  [PUB] No new results.')

        # Check for missing results
        missing = check_missing_results(matches)
        if missing:
            print(f'  [PUB] ⚠️ {len(missing)} matches missing results')

        # 4. Build production data
        all_matches = parse_cup_txt()
        standings = calculate_standings(all_matches)

        # match_data.json
        match_data = []
        for m in all_matches:
            bj_date, bj_time, bj_label, utc_ts = to_beijing_time(
                m['date'], m.get('time', ''), m.get('tz', ''))
            match_data.append({
                'date': bj_date, 'time': bj_time, 'tz': 'UTC+8',
                'utc_ts': utc_ts, 'time_label': bj_label,
                'venue_tz': m.get('tz', ''),
                'home_team': m['home_team'],
                'home_team_cn': team_cn(m['home_team']),
                'away_team': m['away_team'],
                'away_team_cn': team_cn(m['away_team']),
                'home_score': m.get('home_score'),
                'away_score': m.get('away_score'),
                'halftime': m.get('halftime'),
                'venue': m.get('venue'),
                'group': m.get('group'),
                'is_result': m.get('is_result', False),
            })

        # Write production files
        DATA_JSON.write_text(json.dumps(match_data, ensure_ascii=False, indent=2), encoding='utf-8')
        STANDINGS_JSON.write_text(json.dumps(standings, ensure_ascii=False, indent=2), encoding='utf-8')
        TEAM_NAMES_JSON.write_text(json.dumps(TEAM_CN, ensure_ascii=False, indent=2), encoding='utf-8')

        # Quality score
        quality = _calc_quality(match_data, standings)

        # Commit & push
        commit_msg = f'Auto-sync: update standings & data'
        if new_results:
            commit_msg = 'Auto-sync: ' + ', '.join(new_results[:5])
            if len(new_results) > 5:
                commit_msg += f' (+{len(new_results)-5} more)'

        pushed = git_commit_and_push(commit_msg)
        result['updated'] = len(updated)
        result['published'] = pushed
        result['quality'] = quality
        result['scored'] = scored + len(updated)
        result['total'] = len(match_data)

    except Exception as e:
        result['errors'].append(str(e))
        print(f'  [PUB] ERROR: {e}')

    return result


def _calc_quality(matches, standings):
    """Calculate a simple quality score 0-100."""
    score = 100
    if len(matches) < 72:
        score -= 20
    utc_missing = sum(1 for m in matches if not m.get('utc_ts'))
    score -= utc_missing
    if len(standings) != 12:
        score -= 10
    return max(0, min(100, score))


# ═══════════════════════════════════════════════════════════════
# PUBLISH LOOP
# ═══════════════════════════════════════════════════════════════

def publish_cycle():
    """Run one publish cycle."""
    print(f'\n  [PUB] Cycle at {datetime.now().strftime("%H:%M:%S")}')
    result = merge_and_build()
    status = '✅' if result['published'] else '❌'
    quality = result.get('quality', '?')
    print(f'  [PUB] {status} published={result["published"]} quality={quality}/100 updated={result["updated"]}')
    return result


def publish_loop():
    """Continuous publish loop."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         OPERATIONAL DB — Publish Pipeline                   ║
║         Validate → Build → Push                             ║
╚══════════════════════════════════════════════════════════════╝
""")
    while True:
        try:
            publish_cycle()
            time.sleep(PUBLISH_INTERVAL)
        except KeyboardInterrupt:
            print('\n  Publish stopped.')
            break
        except Exception as e:
            print(f'  [PUB ERROR] {e}')
            time.sleep(30)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true')
    p.add_argument('--loop', action='store_true')
    args = p.parse_args()
    if args.once:
        publish_cycle()
    elif args.loop:
        publish_loop()
    else:
        publish_loop()
