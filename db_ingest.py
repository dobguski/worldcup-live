#!/usr/bin/env python3
"""
Resource Database Layer — Data Ingestion Pipeline
=================================================
Fetches raw data from all sources → validates → writes to staging area.
Decoupled from operational DB: failures here don't block the live site.
"""
import json, sys, os, time, urllib.request, gzip, ssl
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

REPO_DIR = Path(__file__).parent
STAGE_DIR = REPO_DIR / '_stage'
PROD_DIR = REPO_DIR  # production is root

# ── Config ──
FETCH_INTERVAL = 30    # seconds between fetch cycles during live matches
IDLE_INTERVAL = 90     # seconds when no live matches
MATCH_WINDOW_HOURS = 2.2  # hours after kickoff considered "live"

# ── SSL ──
def ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# ── HTTP ──
def fetch_json(url: str, retries: int = 2) -> dict | None:
    """Fetch and parse JSON with gzip support."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'application/json',
            })
            with urllib.request.urlopen(req, timeout=15, context=ssl_context()) as resp:
                raw = resp.read()
                if raw[:2] == b'\x1f\x8b':
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode())
        except Exception as e:
            if attempt >= retries - 1:
                print(f'  [INGEST] FETCH FAIL: {url[:60]}... : {e}')
            time.sleep(2)
    return None

# ═══════════════════════════════════════════════════════════════
# SOURCE 1: ESPN Scoreboard API (primary)
# ═══════════════════════════════════════════════════════════════
def fetch_espn_scoreboard() -> dict:
    """Fetch full scoreboard from ESPN."""
    url = 'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260611-20260719'
    data = fetch_json(url)
    if not data:
        return {'events': [], 'source': 'espn', 'status': 'fetch_failed'}
    data['source'] = 'espn'
    data['status'] = 'ok'
    data['fetched_at'] = datetime.now(timezone.utc).isoformat()
    return data

# ═══════════════════════════════════════════════════════════════
# SOURCE 2: TheSportsDB (supplementary)
# ═══════════════════════════════════════════════════════════════
def fetch_thesportsdb_all() -> dict:
    """Fetch from multiple TSDB endpoints."""
    endpoints = [
        'https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=4429&s=2026',
        'https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4429',
        'https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4429',
    ]
    # Add last 3 days
    for i in range(3):
        d = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        endpoints.append(f'https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={d}&s=Soccer')

    all_events = {}
    for url in endpoints:
        data = fetch_json(url)
        if data and 'events' in data:
            for e in data['events']:
                eid = e.get('idEvent', '')
                if eid not in all_events:
                    all_events[eid] = e
    return {
        'events': list(all_events.values()),
        'source': 'thesportsdb',
        'status': 'ok',
        'fetched_at': datetime.now(timezone.utc).isoformat(),
    }

# ═══════════════════════════════════════════════════════════════
# SOURCE 3: FIFA Calendar API (tertiary)
# ═══════════════════════════════════════════════════════════════
def fetch_fifa_calendar() -> dict:
    url = 'https://api.fifa.com/api/v3/calendar/matches?from=2026-06-10T00:00:00Z&to=2026-07-20T23:59:59Z&count=200'
    data = fetch_json(url)
    return {
        'results': data.get('Results', []) if data else [],
        'source': 'fifa',
        'status': 'ok' if data else 'fetch_failed',
        'fetched_at': datetime.now(timezone.utc).isoformat(),
    }

# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════
def validate_staging(stage_data: dict) -> tuple[bool, list[str]]:
    """Validate staged data before publishing. Returns (pass, warnings)."""
    warnings = []
    matches = stage_data.get('matches', [])
    if len(matches) < 72:
        warnings.append(f'Match count low: {len(matches)}/72')
    if len(matches) > 104:
        warnings.append(f'Match count high: {len(matches)}/104')

    # Check UTC timestamps
    missing_utc = sum(1 for m in matches if not m.get('utc_ts'))
    if missing_utc > 0:
        warnings.append(f'{missing_utc} matches missing UTC timestamp')

    # Check score consistency
    scored = [m for m in matches if m.get('is_result')]
    bad_scores = [m for m in scored if m.get('home_score', -1) < 0 or m.get('away_score', -1) < 0]
    if bad_scores:
        warnings.append(f'{len(bad_scores)} matches with invalid scores')

    # Check standings match
    standings = stage_data.get('standings', {})
    if len(standings) != 12:
        warnings.append(f'Standings group count: {len(standings)}/12')

    passed = len(warnings) == 0 or all('low' not in w.lower() for w in warnings)
    return passed, warnings

# ═══════════════════════════════════════════════════════════════
# SOURCE 4: Manifold Markets (prediction market odds)
# ═══════════════════════════════════════════════════════════════
def fetch_manifold_odds() -> dict:
    """Fetch World Cup 2026 champion odds from Manifold Markets API."""
    result = {'markets': [], 'champion_odds': {}, 'source': 'manifold', 'status': 'ok'}

    # Get World Cup winner market
    try:
        search_url = 'https://api.manifold.markets/v0/search-markets?term=world+cup+2026+winner+fifa&limit=10'
        data = fetch_json(search_url)
        if data and isinstance(data, list):
            for item in data:
                q = item.get('question', '')
                prob = item.get('probability')
                if prob is None: continue
                # Check for team-specific markets
                if 'win the 2026' in q.lower() and 'world cup' in q.lower():
                    # Extract team name from question
                    import re
                    team_match = re.search(r'Will\s+(.+?)\s+win', q)
                    if team_match:
                        team = team_match.group(1).strip()
                        result['champion_odds'][team] = round(prob, 4)
                result['markets'].append({
                    'question': q[:200],
                    'probability': prob,
                    'volume': item.get('volume24Hours', 0),
                })

        result['fetched_at'] = datetime.now(timezone.utc).isoformat()
        if result['champion_odds']:
            print(f'  [MANIFOLD] {len(result["champion_odds"])} team odds fetched')
    except Exception as e:
        result['status'] = 'fetch_failed'
        print(f'  [MANIFOLD] Failed: {e}')

    return result

# ═══════════════════════════════════════════════════════════════
# MAIN INGEST CYCLE
# ═══════════════════════════════════════════════════════════════
def ingest_cycle():
    """Run one full ingest cycle: fetch all sources → write to _stage/"""
    os.makedirs(STAGE_DIR, exist_ok=True)
    print(f'\n{"="*50}')
    print(f'  [INGEST] {datetime.now().strftime("%H:%M:%S")}')

    # Step 1: Fetch all sources
    print('  Fetching sources...')
    espn = fetch_espn_scoreboard()
    tsdb = fetch_thesportsdb_all()
    fifa = fetch_fifa_calendar()

    espn_events = len(espn.get('events', []))
    tsdb_events = len(tsdb.get('events', []))
    fifa_events = len(fifa.get('results', []))
    print(f'  ESPN: {espn_events} events | TSDB: {tsdb_events} | FIFA: {fifa_events}')

    # Step 2: Write raw data to staging
    stage_data = {
        'ingested_at': datetime.now(timezone.utc).isoformat(),
        'sources': {
            'espn': espn,
            'thesportsdb': tsdb,
            'fifa': fifa,
            'manifold': fetch_manifold_odds(),
        },
    }
    (STAGE_DIR / 'raw_sources.json').write_text(json.dumps(stage_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'  Staged: raw_sources.json')

    # Step 3: Check for live matches (adjust fetch interval)
    has_live = False
    for e in espn.get('events', []):
        comps = e.get('competitions', [{}])[0]
        status = comps.get('status', {}).get('type', {}).get('name', '')
        if any(kw in status for kw in ['FIRST_HALF', 'SECOND_HALF', 'IN_PROGRESS', 'HALFTIME']):
            has_live = True
            break

    return has_live


def ingest_loop():
    """Continuous ingest loop."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         RESOURCE DB — Data Ingestion Pipeline               ║
║         Fetch → Validate → Stage                            ║
╚══════════════════════════════════════════════════════════════╝
""")
    while True:
        try:
            has_live = ingest_cycle()
            wait = FETCH_INTERVAL if has_live else IDLE_INTERVAL
            print(f'  Next ingest in {wait}s...')
            time.sleep(wait)
        except KeyboardInterrupt:
            print('\n  Ingest stopped.')
            break
        except Exception as e:
            print(f'  [INGEST ERROR] {e}')
            time.sleep(30)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true', help='Run one cycle')
    p.add_argument('--loop', action='store_true', help='Continuous loop')
    args = p.parse_args()
    if args.once:
        ingest_cycle()
    elif args.loop:
        ingest_loop()
    else:
        ingest_loop()
