#!/usr/bin/env python3
"""Parse squad_data/*.md files and update player_details.json + teams.json"""
import json, re, sys, os
from collections import OrderedDict
sys.stdout.reconfigure(encoding='utf-8')

SQUAD_DIR = os.path.join(os.path.dirname(__file__), 'squad_data')

def parse_md_file(path):
    """Parse a group_*_teams.md file and extract team + player data."""
    text = open(path, encoding='utf-8').read()
    teams = OrderedDict()
    current_team = None
    current_section = None
    in_table = False
    table_headers = []

    for line in text.split('\n'):
        line = line.rstrip()

        # Team header: ## 🇲🇽 Mexico / 墨西哥
        m = re.match(r'^##\s+.*?(\w[\w\s&]+?)\s*/\s*(.+?)$', line)
        if not m:
            m = re.match(r'^##\s+.*?(\w[\w\s&]+)\s*$', line)
            if m:
                teams[m.group(1).strip()] = {'name_en': m.group(1).strip(), 'name_cn': '', 'players': [], 'meta': {}}
                current_team = m.group(1).strip()
                continue
        else:
            teams[m.group(1).strip()] = {'name_en': m.group(1).strip(), 'name_cn': m.group(2).strip(), 'players': [], 'meta': {}}
            current_team = m.group(1).strip()
            continue

        if not current_team:
            continue

        # Meta rows: | **Key** | Value |
        meta_m = re.match(r'^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', line)
        if meta_m:
            key = meta_m.group(1).strip()
            val = meta_m.group(2).strip()
            teams[current_team]['meta'][key] = val
            continue

        # Section headers
        if '门将' in line or 'Goalkeeper' in line.title():
            current_section = 'GK'
            in_table = False
            continue
        if '后卫' in line or 'Defender' in line.title():
            current_section = 'DF'
            in_table = False
            continue
        if '中场' in line or 'Midfielder' in line.title():
            current_section = 'MF'
            in_table = False
            continue
        if '前锋' in line or 'Forward' in line.title():
            current_section = 'FW'
            in_table = False
            continue

        # Player table rows: | # | Name CN Name EN | Age | Club CN Club EN | League |
        # Clean bold markers first
        clean = line.replace('**', '')
        player_m = re.match(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|', clean)
        if player_m:
            num = player_m.group(1)
            name_raw = player_m.group(2).strip()
            age = player_m.group(3)
            club_raw = player_m.group(4).strip()
            league = player_m.group(5).strip()

            # Parse name: 中文名 English Name
            # Split Chinese chars from Latin chars
            name_cn = ''
            name_en = ''
            # Try to split at the Chinese-Latin boundary
            parts = re.split(r'\s{2,}', name_raw)
            if len(parts) >= 2:
                name_cn = parts[0].replace('**','').strip()
                name_en = parts[1].replace('**','').strip()
            else:
                # Try char by char
                cn_chars = []
                en_chars = []
                in_en = False
                for ch in name_raw:
                    if ord(ch) > 127:
                        if in_en and cn_chars:
                            name_cn = ''.join(cn_chars).strip().replace('**','')
                            name_en = ''.join(en_chars).strip().replace('**','')
                            cn_chars = [ch]
                            en_chars = []
                        cn_chars.append(ch)
                        in_en = False
                    else:
                        en_chars.append(ch)
                        in_en = True
                if cn_chars:
                    name_cn = (name_cn + ''.join(cn_chars)).strip().replace('**','')
                if en_chars:
                    name_en = (name_en + ''.join(en_chars)).strip().replace('**','')
                if not name_cn:
                    name_cn = name_en
                if not name_en:
                    name_en = name_cn

            # Parse club: 中文名 English Name
            club_cn, club_en = '', ''
            parts = re.split(r'\s{2,}', club_raw)
            if len(parts) >= 2:
                club_cn = parts[0].strip()
                club_en = parts[1].strip()
            else:
                cn = []; en = []
                in_en = False
                for ch in club_raw:
                    if ord(ch) > 127:
                        cn.append(ch); in_en = False
                    else:
                        en.append(ch); in_en = True
                club_cn = ''.join(cn).strip()
                club_en = ''.join(en).strip()
                if not club_cn: club_cn = club_en
                if not club_en: club_en = club_cn

            # Determine position from current section
            pos_map = {'GK': ('Goalkeeper','门将'), 'DF': ('Defender','后卫'), 'MF': ('Midfielder','中场'), 'FW': ('Forward','前锋')}
            pos, pos_cn = pos_map.get(current_section, ('',''))

            teams[current_team]['players'].append({
                'number': num,
                'name': name_en,
                'name_cn': name_cn,
                'age': int(age) if age.isdigit() else None,
                'position': pos,
                'position_cn': pos_cn,
                'club': club_en,
                'club_cn': club_cn,
                'league': league,
            })

    return teams

def update_database():
    """Parse all MD files and update JSON databases."""
    all_teams = {}
    for f in sorted(os.listdir(SQUAD_DIR)):
        if f.startswith('group_') and f.endswith('.md'):
            path = os.path.join(SQUAD_DIR, f)
            print(f'  Parsing {f}...')
            teams = parse_md_file(path)
            all_teams.update(teams)
            for name, data in teams.items():
                print(f'    {data["name_cn"]}: {len(data["players"])} players')

    total_players = sum(len(t['players']) for t in all_teams.values())
    print(f'\n  Total: {len(all_teams)} teams, {total_players} players')

    # Update player_details.json
    details = {}
    try:
        details = json.load(open('player_details.json', encoding='utf-8'))
    except:
        pass

    new_count = 0
    updated_count = 0
    for team_name, team_data in all_teams.items():
        for p in team_data['players']:
            en_name = p['name']
            if not en_name:
                continue
            old = details.get(en_name, {})
            was_empty = not old
            # Update/add all fields
            old['name'] = en_name
            old['name_cn'] = p.get('name_cn', old.get('name_cn', ''))
            old['age'] = p.get('age') or old.get('age')
            old['birth_date'] = p.get('birth_date') or old.get('birth_date', '')
            old['position'] = p.get('position') or old.get('position', '')
            old['position_cn'] = p.get('position_cn') or old.get('position_cn', '')
            old['club'] = p.get('club') or old.get('club', '')
            old['club_cn'] = p.get('club_cn') or old.get('club_cn', '')
            old['number'] = p.get('number') or old.get('number', '')
            old['nationality_team'] = team_name
            details[en_name] = old
            if was_empty:
                new_count += 1
            else:
                updated_count += 1

    json.dump(details, open('player_details.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    # Update wiki_squads.json
    wiki = json.load(open('wiki_squads.json', encoding='utf-8'))
    for team_name, team_data in all_teams.items():
        # Map team name
        mapped = None
        for wname in wiki:
            if team_name.lower() in wname.lower() or wname.lower() in team_name.lower():
                mapped = wname
                break
        if not mapped:
            mapped = team_name
            if mapped not in wiki:
                wiki[mapped] = {'coach': '', 'players': []}

        players = []
        for p in team_data['players']:
            players.append({
                'number': p['number'],
                'name': p['name'],
                'name_cn': p['name_cn'],
                'position': p['position'],
                'position_cn': p['position_cn'],
                'club': p['club'],
                'club_cn': p['club_cn'],
            })
        wiki[mapped]['players'] = players

    json.dump(wiki, open('wiki_squads.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    # Update teams.json
    teams_db = json.load(open('teams.json', encoding='utf-8'))
    for team_name, team_data in all_teams.items():
        mapped = None
        for tname in teams_db:
            if team_name.lower() in tname.lower() or tname.lower() in team_name.lower():
                mapped = tname
                break
        if mapped:
            # Update players from MD data
            md_players = []
            for p in team_data['players']:
                md_players.append({
                    'number': p['number'],
                    'name': p['name'],
                    'name_cn': p['name_cn'],
                    'position': p['position'],
                    'position_cn': p['position_cn'],
                    'club': p['club'],
                    'club_cn': p['club_cn'],
                })
            old_count = len(teams_db[mapped].get('players', []))
            teams_db[mapped]['players'] = md_players
            meta = team_data.get('meta', {})
            if meta.get('FIFA 排名 / Ranking', ''):
                teams_db[mapped]['fifa_ranking'] = meta['FIFA 排名 / Ranking']
            if meta.get('主教练 / Head Coach', ''):
                teams_db[mapped]['coach'] = meta['主教练 / Head Coach']

    json.dump(teams_db, open('teams.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

    total = sum(len(t['players']) for t in teams_db.values())
    with_age = sum(1 for t in teams_db.values() for p in t['players'] if details.get(p.get('name',''),{}).get('age'))
    print(f'  player_details.json: {len(details)} players ({new_count} new, {updated_count} updated)')
    print(f'  teams.json: {len(teams_db)} teams, {total} players')
    print(f'  With age: {with_age}/{total}')

if __name__ == '__main__':
    update_database()
