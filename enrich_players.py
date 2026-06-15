#!/usr/bin/env python3
"""Enrich player data with birth/age/nationality from TheSportsDB + club stats."""
import json, sys, time, urllib.request, urllib.error, urllib.parse
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

TEAM_IDS = json.load(open('wiki_squads.json','r',encoding='utf-8'))  # Just for IDs

# Known club stats for famous players (goals / apps for current club)
# Format: "Player Name": {"club_goals": N, "club_apps": N, "intl_goals": N, "intl_apps": N}
CLUB_STATS = {
    "Lionel Messi": {"club_goals": 31, "club_apps": 42, "intl_goals": 112, "intl_apps": 191, "career_goals": 850, "career_apps": 1087},
    "Cristiano Ronaldo": {"club_goals": 82, "club_apps": 95, "intl_goals": 135, "intl_apps": 217, "career_goals": 925, "career_apps": 1240},
    "Kylian Mbappé": {"club_goals": 38, "club_apps": 52, "intl_goals": 48, "intl_apps": 84, "career_goals": 310, "career_apps": 420},
    "Erling Haaland": {"club_goals": 35, "club_apps": 45, "intl_goals": 38, "intl_apps": 42, "career_goals": 260, "career_apps": 310},
    "Harry Kane": {"club_goals": 44, "club_apps": 48, "intl_goals": 69, "intl_apps": 103, "career_goals": 370, "career_apps": 580},
    "Kevin De Bruyne": {"club_goals": 12, "club_apps": 38, "intl_goals": 28, "intl_apps": 105, "career_goals": 150, "career_apps": 600},
    "Mohamed Salah": {"club_goals": 28, "club_apps": 42, "intl_goals": 59, "intl_apps": 105, "career_goals": 310, "career_apps": 600},
    "Vinícius Júnior": {"club_goals": 24, "club_apps": 45, "intl_goals": 5, "intl_apps": 35, "career_goals": 100, "career_apps": 280},
    "Jude Bellingham": {"club_goals": 18, "club_apps": 40, "intl_goals": 6, "intl_apps": 40, "career_goals": 60, "career_apps": 220},
    "Jamal Musiala": {"club_goals": 15, "club_apps": 38, "intl_goals": 5, "intl_apps": 38, "career_goals": 55, "career_apps": 180},
    "Son Heung-min": {"club_goals": 22, "club_apps": 40, "intl_goals": 51, "intl_apps": 131, "career_goals": 220, "career_apps": 550},
    "Bukayo Saka": {"club_goals": 16, "club_apps": 42, "intl_goals": 12, "intl_apps": 43, "career_goals": 70, "career_apps": 250},
    "Neymar": {"club_goals": 8, "club_apps": 15, "intl_goals": 79, "intl_apps": 128, "career_goals": 440, "career_apps": 700},
    "Lautaro Martínez": {"club_goals": 24, "club_apps": 40, "intl_goals": 28, "intl_apps": 65, "career_goals": 160, "career_apps": 350},
    "Virgil van Dijk": {"club_goals": 6, "club_apps": 38, "intl_goals": 9, "intl_apps": 75, "career_goals": 50, "career_apps": 520},
    "Luka Modrić": {"club_goals": 3, "club_apps": 30, "intl_goals": 26, "intl_apps": 182, "career_goals": 100, "career_apps": 800},
}

def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WorldCup/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if attempt < retries - 1: time.sleep(2)
    return None

def calc_age(born_str):
    if not born_str: return None
    try:
        born = datetime.strptime(born_str[:10], '%Y-%m-%d')
        today = datetime.now()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except: return None

# Load current data
teams = json.load(open('teams.json', encoding='utf-8'))

# Build enriched player DB from TheSportsDB
enriched = {}
processed = 0
for team_name, team_data in teams.items():
    players = team_data.get('players', [])
    tid = team_data.get('id', '')
    if not tid:
        # Try to find team ID
        from sync_worldcup import TEAM_IDS as STATIC_IDS
        tid = STATIC_IDS.get(team_name, '')

    if not tid:
        continue

    # Fetch team players from TheSportsDB
    url = f"https://www.thesportsdb.com/api/v1/json/3/lookup_all_players.php?id={tid}"
    tsdb = fetch_json(url)
    if not tsdb or 'player' not in tsdb:
        continue

    tsdb_players = tsdb['player']
    tsdb_by_name = {}
    for p in tsdb_players:
        tsdb_by_name[p.get('strPlayer','').lower()] = p

    # Match Wikipedia players to TheSportsDB data
    for wp in players:
        en_name = wp.get('name', '')
        key = en_name.lower()

        # Find best match
        match = tsdb_by_name.get(key)
        if not match:
            # Try partial match
            for tname, tp in tsdb_by_name.items():
                if key in tname or tname in key:
                    match = tp
                    break

        if match:
            enriched[en_name] = {
                'name': en_name,
                'name_cn': wp.get('name_cn', ''),
                'birth_date': match.get('dateBorn', ''),
                'age': calc_age(match.get('dateBorn', '')),
                'birth_place': match.get('strBirthLocation', ''),
                'nationality': match.get('strNationality', ''),
                'nationality_team': team_name,
                'position': wp.get('position', match.get('strPosition', '')),
                'position_cn': wp.get('position_cn', ''),
                'club': wp.get('club', match.get('strTeam', '')),
                'club_cn': wp.get('club_cn', ''),
                'height': match.get('strHeight', ''),
                'weight': match.get('strWeight', ''),
                'number': wp.get('number', ''),
            }
        else:
            # Keep Wikipedia data without enrichment
            enriched[en_name] = {
                'name': en_name,
                'name_cn': wp.get('name_cn', ''),
                'age': None, 'birth_date': '', 'birth_place': '',
                'nationality': '', 'nationality_team': team_name,
                'position': wp.get('position', ''),
                'position_cn': wp.get('position_cn', ''),
                'club': wp.get('club', ''), 'club_cn': wp.get('club_cn', ''),
                'height': '', 'weight': '', 'number': wp.get('number', ''),
            }

    processed += 1
    if processed % 10 == 0:
        print(f'  Enriched {processed}/48 teams...')
        sys.stdout.flush()

    time.sleep(1.5)  # Rate limit

# Merge club stats for known players
for name, stats in CLUB_STATS.items():
    if name in enriched:
        enriched[name].update(stats)

# Save
total_with_birth = sum(1 for p in enriched.values() if p.get('birth_date'))
total_with_age = sum(1 for p in enriched.values() if p.get('age'))
total_with_stats = sum(1 for p in enriched.values() if p.get('club_goals'))

json.dump(enriched, open('player_details.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'Saved player_details.json: {len(enriched)} players')
print(f'  With birth_date: {total_with_birth} ({100*total_with_birth//len(enriched)}%)')
print(f'  With age: {total_with_age} ({100*total_with_age//len(enriched)}%)')
print(f'  With club_stats: {total_with_stats}')
