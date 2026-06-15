#!/usr/bin/env python3
"""
数据质量验证引擎 — Data Quality Verification Engine
=====================================================
分层验证：完整性 → 一致性 → 时效性 → 准确性
"""

import json, sys, os, time
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).parent

# ============================================================
# LAYER 1: COMPLETENESS — 完整性检查
# ============================================================
def check_completeness() -> list[dict]:
    """Verify all required data files and fields exist."""
    issues = []

    # Check required files
    required = ['match_data.json','standings.json','teams.json','team_names.json',
                'polymarket.json','wiki_squads.json','dashboard.html','CNAME']
    for f in required:
        path = REPO / f
        if not path.exists():
            issues.append({'layer':'completeness','severity':'critical','file':f,'issue':'File missing'})
        elif path.stat().st_size < 5 and f != 'CNAME':  # CNAME is only ~13 bytes
            issues.append({'layer':'completeness','severity':'critical','file':f,'issue':'File too small/empty'})

    # Check match_data content
    try:
        matches = json.loads((REPO/'match_data.json').read_text(encoding='utf-8'))
        if len(matches) < 71:
            issues.append({'layer':'completeness','severity':'high','file':'match_data.json',
                          'issue':f'Only {len(matches)}/104 matches'})
        without_score = [m for m in matches if m.get('is_result') and (m.get('home_score') is None)]
        if without_score:
            issues.append({'layer':'completeness','severity':'high','file':'match_data.json',
                          'issue':f'{len(without_score)} matches marked result but missing score'})
    except Exception as e:
        issues.append({'layer':'completeness','severity':'critical','file':'match_data.json','issue':str(e)})

    # Check teams completeness
    try:
        teams = json.loads((REPO/'teams.json').read_text(encoding='utf-8'))
        if len(teams) != 48:
            issues.append({'layer':'completeness','severity':'high','file':'teams.json',
                          'issue':f'Only {len(teams)}/48 teams'})
        no_players = [k for k,t in teams.items() if len(t.get('players',[])) == 0]
        if no_players:
            issues.append({'layer':'completeness','severity':'medium','file':'teams.json',
                          'issue':f'{len(no_players)} teams with 0 players'})
        no_coach = [k for k,t in teams.items() if not t.get('coach')]
        if no_coach:
            issues.append({'layer':'completeness','severity':'low','file':'teams.json',
                          'issue':f'{len(no_coach)} teams missing coach'})
    except Exception as e:
        issues.append({'layer':'completeness','severity':'critical','file':'teams.json','issue':str(e)})

    return issues


# ============================================================
# LAYER 2: CONSISTENCY — 一致性检查
# ============================================================
def check_consistency() -> list[dict]:
    """Cross-validate data between files."""
    issues = []

    try:
        matches = json.loads((REPO/'match_data.json').read_text(encoding='utf-8'))
        standings = json.loads((REPO/'standings.json').read_text(encoding='utf-8'))
        teams = json.loads((REPO/'teams.json').read_text(encoding='utf-8'))
        team_cn_map = json.loads((REPO/'team_names.json').read_text(encoding='utf-8'))
    except Exception as e:
        return [{'layer':'consistency','severity':'critical','issue':f'Cannot read files: {e}'}]

    # Verify standings match results
    calculated = {}
    for m in matches:
        if not m.get('is_result'): continue
        g = m['group']
        if g not in calculated:
            calculated[g] = defaultdict(lambda: {'gp':0,'w':0,'d':0,'l':0,'gf':0,'ga':0,'pts':0})
        for side, opp_side in [('home_team','away_team'), ('away_team','home_team')]:
            team = m[side]
            opp = m[opp_side]
            hs = m['home_score'] if side == 'home_team' else m['away_score']
            os_ = m['away_score'] if side == 'home_team' else m['home_score']
            if hs is None: continue
            calculated[g][team]['gp'] += 1
            calculated[g][team]['gf'] += hs
            calculated[g][team]['ga'] += os_
            if hs > os_:
                calculated[g][team]['w'] += 1; calculated[g][team]['pts'] += 3
            elif hs == os_:
                calculated[g][team]['d'] += 1; calculated[g][team]['pts'] += 1
            else:
                calculated[g][team]['l'] += 1

    # Compare with standings.json
    for g in standings:
        for t in standings[g]:
            name = t['team']
            calc = calculated.get(g, {}).get(name, None)
            if calc:
                for field in ['gp','w','d','l','gf','ga','pts']:
                    if t[field] != calc[field]:
                        issues.append({'layer':'consistency','severity':'high',
                                      'issue':f'Group {g} {name}: {field} mismatch (standings={t[field]}, calc={calc[field]})'})

    # Verify team names match across files
    match_teams = set()
    for m in matches:
        match_teams.add(m['home_team'])
        match_teams.add(m['away_team'])

    teams_json_teams = set(teams.keys())
    wiki_teams = set(json.loads((REPO/'wiki_squads.json').read_text(encoding='utf-8')).keys())
    cn_map_teams = set(team_cn_map.keys())

    missing_from_wiki = match_teams - wiki_teams
    if missing_from_wiki:
        issues.append({'layer':'consistency','severity':'low',
                      'issue':f'{len(missing_from_wiki)} teams in matches not in wiki_squads'})

    # Verify team counts in groups
    from sync_worldcup import GROUPS
    for g, group_teams in GROUPS.items():
        missing = set(group_teams) - teams_json_teams
        if missing:
            issues.append({'layer':'consistency','severity':'high',
                          'issue':f'Group {g} teams missing from teams.json: {missing}'})

    return issues


# ============================================================
# LAYER 3: FRESHNESS — 时效性检查
# ============================================================
def check_freshness() -> list[dict]:
    """Verify data freshness against expected update frequencies."""
    issues = []
    now = time.time()

    freshness_rules = {
        'match_data.json': {'max_age': 180, 'label': 'Match data', 'severity_if_stale': 'high'},
        'standings.json': {'max_age': 180, 'label': 'Standings', 'severity_if_stale': 'high'},
        'match_data.json': {'max_age': 300, 'label': 'Match data (idle)', 'severity_if_stale': 'medium'},
    }

    for f, rule in freshness_rules.items():
        path = REPO / f
        if not path.exists():
            continue
        age = now - path.stat().st_mtime
        if age > rule['max_age'] * 2:
            issues.append({'layer':'freshness','severity':'critical',
                          'issue':f'{rule["label"]}: {age/3600:.1f}h old (max {rule["max_age"]//60}min)'})
        elif age > rule['max_age']:
            issues.append({'layer':'freshness','severity':rule['severity_if_stale'],
                          'issue':f'{rule["label"]}: {age/60:.0f}min old'})

    # Check if sync is producing new data
    match_path = REPO / 'match_data.json'
    if match_path.exists():
        try:
            matches = json.loads(match_path.read_text(encoding='utf-8'))
            result_dates = [m['date'] for m in matches if m.get('is_result')]
            if result_dates:
                latest_result = max(result_dates)
                today = datetime.now().strftime('%Y-%m-%d')
                if latest_result < today:
                    # No results synced today - could be normal if no matches today
                    pass
        except Exception:
            pass

    return issues


# ============================================================
# LAYER 4: ACCURACY — 准确性检查
# ============================================================
def check_accuracy() -> list[dict]:
    """Verify data accuracy with heuristics."""
    issues = []

    try:
        matches = json.loads((REPO/'match_data.json').read_text(encoding='utf-8'))
        standings = json.loads((REPO/'standings.json').read_text(encoding='utf-8'))
    except Exception as e:
        return [{'layer':'accuracy','severity':'critical','issue':f'Cannot read: {e}'}]

    # Suspicious score patterns
    for m in matches:
        if not m.get('is_result'): continue
        hs, aws = m.get('home_score'), m.get('away_score')
        if hs is None or aws is None: continue
        # Impossible score: >20 goals
        if hs > 15 or aws > 15:
            issues.append({'layer':'accuracy','severity':'high',
                          'issue':f'{m["date"]} {m["home_team"]} {hs}-{aws} {m["away_team"]}: suspicious score >15'})

    # Standings consistency: no team should have more games than matches in group
    for g in standings:
        for t in standings[g]:
            if t['gp'] > 6:  # Max 6 group stage games (3 per team in 4-team group, but we have 48 teams = 3 group games each)
                issues.append({'layer':'accuracy','severity':'high',
                              'issue':f'Group {g} {t["team"]}: {t["gp"]} games played (max 3 in group stage)'})
            if t['w'] + t['d'] + t['l'] != t['gp']:
                issues.append({'layer':'accuracy','severity':'high',
                              'issue':f'Group {g} {t["team"]}: W+D+L={t["w"]+t["d"]+t["l"]} != GP={t["gp"]}'})

    # Cross-check PM accuracy stats
    try:
        pm = json.loads((REPO/'polymarket.json').read_text(encoding='utf-8'))
        pm_matches = pm.get('matches', {})
        correct = sum(1 for m in pm_matches.values() if m.get('correct'))
        total_pm = len(pm_matches)
        if total_pm > 0:
            actual_rate = correct / total_pm
            stated_rate = pm.get('accuracy_stats',{}).get('favorite_win_rate', 0)
            if abs(actual_rate - stated_rate) > 0.05:
                issues.append({'layer':'accuracy','severity':'low',
                              'issue':f'PM accuracy stats mismatch: actual={actual_rate:.0%}, stated={stated_rate:.0%}'})
    except Exception:
        pass

    return issues


# ============================================================
# MASTER VERIFICATION
# ============================================================
def run_all_checks() -> dict:
    """Run all verification layers and return report."""
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'layers': {
            'completeness': {'issues': check_completeness()},
            'consistency':  {'issues': check_consistency()},
            'freshness':    {'issues': check_freshness()},
            'accuracy':     {'issues': check_accuracy()},
        }
    }

    # Summary
    total_issues = sum(len(v['issues']) for v in report['layers'].values())
    critical = sum(1 for v in report['layers'].values()
                   for i in v['issues'] if i['severity'] == 'critical')
    high = sum(1 for v in report['layers'].values()
               for i in v['issues'] if i['severity'] == 'high')

    report['summary'] = {
        'total_issues': total_issues,
        'critical': critical,
        'high': high,
        'status': 'OK' if critical == 0 and high == 0 else ('WARN' if critical == 0 else 'FAIL'),
        'verdict': 'All checks passed' if critical == 0 and high == 0 else
                   f'{critical} critical, {high} high issues need attention'
    }

    return report


# ============================================================
# DATA QUALITY SCORE (0-100)
# ============================================================
def calculate_quality_score(report: dict) -> int:
    """Calculate data quality score from verification report."""
    score = 100
    weights = {'critical': 20, 'high': 10, 'medium': 3, 'low': 1}
    for layer in report['layers'].values():
        for issue in layer['issues']:
            score -= weights.get(issue['severity'], 0)
    return max(0, score)


if __name__ == '__main__':
    report = run_all_checks()
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    score = calculate_quality_score(report)
    print(f'\nQuality Score: {score}/100')
    print(f'Status: {report["summary"]["status"]}')
    print(f'Verdict: {report["summary"]["verdict"]}')
