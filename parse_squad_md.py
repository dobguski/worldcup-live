#!/usr/bin/env python3
"""Parse squad_data/*.md files — extract ALL valuable info: dual nationals, key stats, historical notes"""
import json, re, sys, os
from collections import OrderedDict
sys.stdout.reconfigure(encoding='utf-8')

SQUAD_DIR = os.path.join(os.path.dirname(__file__), 'squad_data')

def parse_md_file(path):
    text = open(path, encoding='utf-8').read()
    teams = OrderedDict()
    current_team = None
    current_section = None
    dual_lines = []
    stats_lines = []
    history_lines = []

    for line in text.split('\n'):
        line = line.rstrip()

        # Team header
        m = re.match(r'^##\s+.*?(\w[\w\s&]+?)\s*/\s*(.+?)$', line)
        if not m:
            m = re.match(r'^##\s+.*?(\w[\w\s&]+)\s*$', line)
            if m:
                current_team = m.group(1).strip()
                teams[current_team] = {'name_en': current_team, 'name_cn': '', 'players': [], 'meta': {},
                                        'dual_nationals': '', 'key_stats': '', 'historical_note': ''}
                dual_lines = []; stats_lines = []; history_lines = []
                current_section = 'overview'
                continue
        else:
            current_team = m.group(1).strip()
            teams[current_team] = {'name_en': current_team, 'name_cn': m.group(2).strip(), 'players': [], 'meta': {},
                                    'dual_nationals': '', 'key_stats': '', 'historical_note': ''}
            dual_lines = []; stats_lines = []; history_lines = []
            current_section = 'overview'
            continue

        if not current_team:
            continue

        # Section detection
        if '双重国籍' in line or 'Dual National' in line:
            current_section = 'dual'
            continue
        if '关键数据' in line or 'Key Stat' in line:
            current_section = 'stats'
            continue
        if '历史看点' in line or 'Historical Note' in line:
            current_section = 'history'
            continue
        if '球队概况' in line or 'Overview' in line:
            current_section = 'overview'
            continue
        if '26人大名单' in line or 'Squad' in line or 'Man Squad' in line:
            current_section = 'squad'
            continue
        if line.startswith('## ') or line.startswith('---'):
            if current_team and (dual_lines or stats_lines or history_lines):
                t = teams[current_team]
                if dual_lines: t['dual_nationals'] = ' '.join(dual_lines).strip()
                if stats_lines: t['key_stats'] = ' '.join(stats_lines).strip()
                if history_lines: t['historical_note'] = ' '.join(history_lines).strip()
            dual_lines = []; stats_lines = []; history_lines = []
            current_section = None
            continue

        # Meta rows
        meta_m = re.match(r'^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', line)
        if meta_m and current_section in ('overview', None):
            key = meta_m.group(1).strip()
            val = meta_m.group(2).strip()
            teams[current_team]['meta'][key] = val
            continue

        # Collect dual/stats/history text
        clean = line.strip()
        if current_section == 'dual' and clean and not clean.startswith('|') and not clean.startswith('#'):
            dual_lines.append(clean)
        elif current_section == 'stats' and clean and not clean.startswith('|') and not clean.startswith('#'):
            stats_lines.append(clean)
        elif current_section == 'history' and clean and not clean.startswith('|') and not clean.startswith('#'):
            history_lines.append(clean)

        # Position sub-sections
        if '门将' in line or 'Goalkeeper' in line.title():
            current_section = 'GK'; continue
        if '后卫' in line or 'Defender' in line.title():
            current_section = 'DF'; continue
        if '中场' in line or 'Midfielder' in line.title():
            current_section = 'MF'; continue
        if '前锋' in line or 'Forward' in line.title():
            current_section = 'FW'; continue

        # Player rows
        clean = line.replace('**', '')
        player_m = re.match(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|', clean)
        if player_m and current_section in ('GK','DF','MF','FW'):
            num = player_m.group(1)
            name_raw = player_m.group(2).strip()
            age = player_m.group(3)
            club_raw = player_m.group(4).strip()
            league = player_m.group(5).strip()

            # Split name CN/EN
            name_cn, name_en = split_bilingual(name_raw)
            # Split club CN/EN
            club_cn, club_en = split_bilingual(club_raw)

            pos_map = {'GK': ('Goalkeeper','门将'), 'DF': ('Defender','后卫'),
                       'MF': ('Midfielder','中场'), 'FW': ('Forward','前锋')}
            pos, pos_cn = pos_map.get(current_section, ('',''))

            teams[current_team]['players'].append({
                'number': num, 'name': name_en, 'name_cn': name_cn,
                'age': int(age) if age.isdigit() else None,
                'position': pos, 'position_cn': pos_cn,
                'club': club_en, 'club_cn': club_cn, 'league': league,
            })

    # Save last team's text sections
    if current_team:
        t = teams[current_team]
        if dual_lines: t['dual_nationals'] = ' '.join(dual_lines).strip()
        if stats_lines: t['key_stats'] = ' '.join(stats_lines).strip()
        if history_lines: t['historical_note'] = ' '.join(history_lines).strip()

    return teams

def split_bilingual(raw):
    """Split '中文名 English Name' into (cn, en) parts."""
    parts = re.split(r'\s{2,}', raw)
    if len(parts) >= 2:
        return parts[0].strip(), ' '.join(parts[1:]).strip()
    cn, en = [], []
    in_en = False
    for ch in raw:
        if ord(ch) > 127:
            cn.append(ch); in_en = False
        else:
            en.append(ch); in_en = True
    rcn = ''.join(cn).strip()
    ren = ''.join(en).strip()
    return (rcn or ren), (ren or rcn)

def update_database():
    all_teams = {}
    for f in sorted(os.listdir(SQUAD_DIR)):
        if f.startswith('group_') and f.endswith('.md'):
            path = os.path.join(SQUAD_DIR, f)
            print(f'  Parsing {f}...')
            teams = parse_md_file(path)
            all_teams.update(teams)
            for name, data in teams.items():
                extra = ''
                if data.get('dual_nationals'): extra += ' [dual]'
                if data.get('key_stats'): extra += ' [stats]'
                if data.get('historical_note'): extra += ' [history]'
                print(f'    {data["name_cn"]}: {len(data["players"])} players{extra}')

    total_players = sum(len(t['players']) for t in all_teams.values())
    print(f'\n  Total: {len(all_teams)} teams, {total_players} players')

    # --- Update player_details.json ---
    details = {}
    try: details = json.load(open('player_details.json', encoding='utf-8'))
    except: pass

    for team_name, team_data in all_teams.items():
        for p in team_data['players']:
            en = p['name']
            if not en: continue
            old = details.get(en, {})
            old['name'] = en
            for field in ['name_cn','age','position','position_cn','club','club_cn','number']:
                if p.get(field): old[field] = p[field]
            old['league'] = p.get('league', old.get('league',''))
            old['nationality_team'] = team_name
            details[en] = old

    json.dump(details, open('player_details.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    # --- Update teams.json with ALL extracted info ---
    teams_db = json.load(open('teams.json', encoding='utf-8'))
    for team_name, team_data in all_teams.items():
        mapped = None
        for tname in teams_db:
            if team_name.lower() in tname.lower() or tname.lower() in team_name.lower():
                mapped = tname; break
        if not mapped: mapped = team_name

        if mapped not in teams_db:
            teams_db[mapped] = {'name_en': mapped, 'name_cn': team_data['name_cn'], 'players': []}

        md_players = []
        for p in team_data['players']:
            md_players.append({
                'number': p['number'], 'name': p['name'], 'name_cn': p['name_cn'],
                'age': p.get('age'), 'position': p['position'], 'position_cn': p['position_cn'],
                'club': p['club'], 'club_cn': p['club_cn'], 'league': p.get('league',''),
            })
        teams_db[mapped]['players'] = md_players

        # Add extracted sections
        if team_data.get('dual_nationals'):
            teams_db[mapped]['dual_nationals'] = team_data['dual_nationals']
        if team_data.get('key_stats'):
            teams_db[mapped]['key_stats'] = team_data['key_stats']
        if team_data.get('historical_note'):
            teams_db[mapped]['historical_note'] = team_data['historical_note']

        # Meta
        meta = team_data.get('meta', {})
        for meta_key in ['FIFA 排名 / Ranking', '主教练 / Head Coach', '队长 / Captain',
                          '球队绰号 / Nickname', '世界杯参赛次数 / Appearances',
                          '历史最佳战绩 / Best Finish']:
            if meta.get(meta_key):
                teams_db[mapped]['meta_' + meta_key] = meta[meta_key]

    json.dump(teams_db, open('teams.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    # --- Update wiki_squads.json ---
    wiki = json.load(open('wiki_squads.json', encoding='utf-8'))
    for team_name, team_data in all_teams.items():
        mapped = None
        for wname in wiki:
            if team_name.lower() in wname.lower() or wname.lower() in team_name.lower():
                mapped = wname; break
        if not mapped: mapped = team_name
        if mapped not in wiki: wiki[mapped] = {'coach': '', 'players': []}
        players = []
        for p in team_data['players']:
            players.append({
                'number': p['number'], 'name': p['name'], 'name_cn': p['name_cn'],
                'age': p.get('age'), 'position': p['position'], 'position_cn': p['position_cn'],
                'club': p['club'], 'club_cn': p['club_cn'], 'league': p.get('league',''),
            })
        wiki[mapped]['players'] = players
    json.dump(wiki, open('wiki_squads.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    # Stats
    dual_count = sum(1 for t in teams_db.values() if t.get('dual_nationals'))
    stats_count = sum(1 for t in teams_db.values() if t.get('key_stats'))
    hist_count = sum(1 for t in teams_db.values() if t.get('historical_note'))
    with_age = sum(1 for t in teams_db.values() for p in t['players'] if p.get('age'))
    total = sum(len(t['players']) for t in teams_db.values())

    print(f'  teams.json: {len(teams_db)} teams, {total} players ({with_age} with age)')
    print(f'  dual_nationals: {dual_count}/48 | key_stats: {stats_count}/48 | historical_note: {hist_count}/48')
    print(f'  player_details.json: {len(details)} entries')

if __name__ == '__main__':
    update_database()
