#!/usr/bin/env python3
"""Goal Scorers Data Pipeline — real-time + daily refresh
- Phase 1 (real-time): Parse cup.txt goal details after each sync
- Phase 2 (daily): Scrape Wikipedia for comprehensive list
- Merge: Wikipedia as base, cup.txt supplements new goals
"""
import json, re, sys, io, os, urllib.request, gzip, ssl
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

def ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def parse_cuptxt_goals(cup_path=None):
    """Parse goal scorers from cup.txt detail lines."""
    if cup_path is None:
        cup_path = os.path.join(REPO, '2026--usa', 'cup.txt')
    goals = Counter()
    if not os.path.exists(cup_path):
        return goals
    with open(cup_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if "'" not in line:
                continue
            scorers = re.findall(r'([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+)+)\s+(\d+)\'', line)
            for name, minute in scorers:
                name = name.strip()
                if len(name) > 5 and name not in ('Penalty','Extra','Time','Half','Full','Goal','Kick'):
                    goals[name] += 1
    return goals

def fetch_name_cn_map():
    """Build English → Chinese name mapping from player_details.json."""
    details_path = os.path.join(REPO, 'player_details.json')
    name_cn = {}
    if os.path.exists(details_path):
        players = json.load(open(details_path, encoding='utf-8'))
        for en, p in players.items():
            if p.get('name_cn'):
                name_cn[en] = p['name_cn']
    return name_cn

def update_goalscorers(cuptxt_goals: Counter, name_cn: dict) -> dict:
    """Update goalscorers.json: merge cup.txt goals into Wikipedia base."""
    gpath = os.path.join(REPO, 'goalscorers.json')

    try:
        goals = json.load(open(gpath, encoding='utf-8'))
    except Exception:
        goals = {'wc2026': [], 'all_time': [], 'total_2026_scorers': 0, 'total_2026_goals': 0}

    existing = {p['name']: i for i, p in enumerate(goals.get('wc2026', []))}

    # Update existing entries with cup.txt counts
    for name, count in cuptxt_goals.items():
        if name in existing:
            goals['wc2026'][existing[name]]['goals'] = count
        else:
            cn = name_cn.get(name, '')
            goals['wc2026'].append({'name': name, 'goals': count, 'name_cn': cn})

    # Re-sort
    goals['wc2026'].sort(key=lambda x: -x['goals'])
    goals['total_2026_scorers'] = len(goals['wc2026'])
    goals['total_2026_goals'] = sum(p['goals'] for p in goals['wc2026'])

    from datetime import datetime
    goals['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')

    json.dump(goals, open(gpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return goals

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--cup-only', action='store_true', help='Only parse cup.txt, skip Wikipedia')
    args = p.parse_args()

    # Phase 1: Real-time from cup.txt
    cuptxt = parse_cuptxt_goals()
    name_cn = fetch_name_cn_map()
    result = update_goalscorers(cuptxt, name_cn)

    new_from_cup = sum(1 for p in result['wc2026'] if p['name'] in cuptxt)
    print(f'[GOALS] cup.txt: {len(cuptxt)} new scorers | total: {len(result["wc2026"])} players | {result["total_2026_goals"]} goals')
    return result

if __name__ == '__main__':
    main()
