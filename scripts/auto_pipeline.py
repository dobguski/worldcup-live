#!/usr/bin/env python3
"""
World Cup Automated Pipeline Monitor
Usage: python scripts/auto_pipeline.py --collect
Collects CLOB champion odds + match results, runs QC validation.
"""
import json, sys, os, io, time, urllib.request, gzip, ssl, re
from datetime import datetime, timezone, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO_DIR)

BLOCKERS = []
WARNINGS = []

def ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    raw = urllib.request.urlopen(req, timeout=15, context=ssl_ctx()).read()
    if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
    return json.loads(raw)

# ═══════════════════════════════════════════════════════════════
# STEP 1: Collect CLOB Champion Odds (Polymarket event/30615)
# ═══════════════════════════════════════════════════════════════
def collect_clob_odds():
    try:
        event = fetch_json('https://gamma-api.polymarket.com/events/30615')
        odds = {}
        for m in event.get('markets', []):
            q = m.get('question', '')
            outcomes = m.get('outcomes', [])
            prices = m.get('outcomePrices', [])
            if isinstance(outcomes, str): outcomes = json.loads(outcomes)
            if isinstance(prices, str): prices = json.loads(prices)
            team_match = re.search(r'Will (.+?) win the 2026', q)
            if not team_match: continue
            for o in outcomes:
                label = o.get('outcome', o) if isinstance(o, dict) else o
                if label.lower() == 'yes':
                    idx = outcomes.index(o)
                    prob = float(prices[idx]) if idx < len(prices) else 0
                    if prob > 0.001:
                        odds[team_match.group(1).strip()] = round(prob, 4)
        print(f'[CLOB] {len(odds)} champion odds collected')
        if len(odds) < 20:
            WARNINGS.append(f'CLOB odds count low: {len(odds)}')
        return odds
    except Exception as e:
        BLOCKERS.append(f'CLOB collection failed: {e}')
        return {}

# ═══════════════════════════════════════════════════════════════
# STEP 2: Collect Match Results
# ═══════════════════════════════════════════════════════════════
def collect_results():
    try:
        mpath = os.path.join(REPO_DIR, 'match_data.json')
        matches = json.load(open(mpath, encoding='utf-8'))
        scored = [m for m in matches if m.get('is_result')]
        now = datetime.now(timezone.utc)
        missing = []
        for m in matches:
            if m.get('is_result'): continue
            if not m.get('utc_ts'): continue
            ko = datetime.strptime(m['utc_ts'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if ko + timedelta(hours=2.5) < now:
                missing.append(f"{m['home_team']} vs {m['away_team']} ({m['date']})")

        print(f'[MATCH] {len(scored)}/{len(matches)} scored')
        if missing:
            WARNINGS.append(f'{len(missing)} past-kickoff matches missing scores')
            for m in missing:
                print(f'  MISSING: {m}')
        if len(scored) < 30:
            BLOCKERS.append(f'Only {len(scored)} matches scored — data gap')
        return scored, missing
    except Exception as e:
        BLOCKERS.append(f'Match collection failed: {e}')
        return [], []

# ═══════════════════════════════════════════════════════════════
# STEP 3: QC Validation
# ═══════════════════════════════════════════════════════════════
def run_qc():
    # Check server
    try:
        resp = urllib.request.urlopen('http://localhost:8888/health', timeout=5)
        h = json.loads(resp.read())
        age = h.get('data_age_min', 999)
        push_fails = h.get('push_failures', 0)
        print(f'[QC] Server: {h["status"]} | data_age={age}min | push_fails={push_fails}')
        if h['status'] == 'stale':
            BLOCKERS.append(f'Data stale: {age}min old')
        if push_fails > 10:
            BLOCKERS.append(f'Push failures: {push_fails}')
        elif push_fails > 3:
            WARNINGS.append(f'Push failures accumulating: {push_fails}')
    except Exception:
        WARNINGS.append('Server health check failed — server may be down')

    # Check push_failures.log
    log_path = os.path.join(REPO_DIR, 'push_failures.log')
    if os.path.exists(log_path):
        lines = open(log_path, encoding='utf-8').readlines()
        recent = [l for l in lines[-5:] if l.strip()]
        if recent:
            print(f'[QC] Recent push failures: {len(recent)}')

    # Check data integrity
    mpath = os.path.join(REPO_DIR, 'match_data.json')
    matches = json.load(open(mpath, encoding='utf-8'))
    utc_missing = sum(1 for m in matches if not m.get('utc_ts'))
    if utc_missing > 0:
        BLOCKERS.append(f'{utc_missing} matches missing UTC timestamps')
    if len(matches) != 72:
        WARNINGS.append(f'Match count: {len(matches)}/72')

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--collect', action='store_true')
    args = p.parse_args()

    print(f'{"="*50}')
    print(f'  Pipeline Monitor — {datetime.now().strftime("%H:%M:%S")}')
    print(f'{"="*50}\n')

    if args.collect:
        odds = collect_clob_odds()
        scored, missing = collect_results()
        run_qc()

        # Update polymarket.json
        if odds:
            pm_path = os.path.join(REPO_DIR, 'polymarket.json')
            pm = json.load(open(pm_path, encoding='utf-8'))
            pm['champion_odds'] = odds
            pm['champion_odds_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            json.dump(pm, open(pm_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print(f'\n[PM] polymarket.json updated ({len(odds)} teams)')

    else:
        # Quick check only
        scored, missing = collect_results()
        run_qc()

    # Report
    print(f'\n{"="*50}')
    if BLOCKERS:
        for b in BLOCKERS:
            print(f'  🔴 BLOCKER: {b}')
    if WARNINGS:
        for w in WARNINGS:
            print(f'  🟡 WARN: {w}')
    if not BLOCKERS and not WARNINGS:
        print(f'  ✅ 管道正常')
    print(f'{"="*50}')

    sys.exit(1 if BLOCKERS else 0)
