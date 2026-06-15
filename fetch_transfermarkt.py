#!/usr/bin/env python3
"""Fetch player data from salimt/football-datasets (Transfermarkt) and match to our 963 players."""
import json, sys, csv, io, urllib.request, time, re
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

BASE = "https://raw.githubusercontent.com/salimt/football-datasets/main/datalake/transfermarkt"

def calc_age(born_str):
    if not born_str: return None
    try:
        born = datetime.strptime(born_str[:10], '%Y-%m-%d')
        today = datetime.now()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except: return None

def download_csv(path):
    """Download a CSV file from GitHub raw."""
    url = f"{BASE}/{path}"
    print(f"  Downloading {path}...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WorldCup/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8')
        except Exception as e:
            if attempt < 2: time.sleep(3)
            else:
                print(f"    Failed: {e}")
                return None

# Step 1: Download player profiles (26MB)
profiles_csv = download_csv("player_profiles/player_profiles.csv")
if not profiles_csv:
    print("ERROR: Cannot download profiles")
    sys.exit(1)

# Step 2: Parse profiles into lookup dict by name
print("  Parsing player profiles...")
reader = csv.DictReader(io.StringIO(profiles_csv))
profiles_by_name = {}
for row in reader:
    name = row.get('player_name', '').strip()
    if name:
        profiles_by_name[name.lower()] = {
            'name': name,
            'birth_date': row.get('date_of_birth', ''),
            'birth_place': row.get('place_of_birth', ''),
            'country_of_birth': row.get('country_of_birth', ''),
            'height': row.get('height', ''),
            'citizenship': row.get('citizenship', ''),  # Can be multiple!
            'position': row.get('position', ''),
            'main_position': row.get('main_position', ''),
            'foot': row.get('foot', ''),
            'current_club': row.get('current_club_name', ''),
        }
print(f"  Profiles loaded: {len(profiles_by_name)}")

# Step 3: Download national team performances (5MB)
nat_csv = download_csv("player_national_performances/player_national_performances.csv")
nat_stats = {}
if nat_csv:
    print("  Parsing national performances...")
    reader = csv.DictReader(io.StringIO(nat_csv))
    for row in reader:
        name = row.get('player_name', '').strip()
        if name not in nat_stats:
            nat_stats[name] = {'intl_goals': 0, 'intl_apps': 0, 'intl_assists': 0}
        nat_stats[name]['intl_goals'] += int(row.get('goals', 0) or 0)
        nat_stats[name]['intl_apps'] += int(row.get('appearances', 0) or 0)
        nat_stats[name]['intl_assists'] += int(row.get('assists', 0) or 0)
    print(f"  National stats loaded: {len(nat_stats)} players")

# Step 4: Load our 963 players and match
details = json.load(open('player_details.json', encoding='utf-8'))
matched = 0
enriched = 0

for en_name, player in details.items():
    key = en_name.lower()
    profile = profiles_by_name.get(key)

    if not profile:
        # Try matching by surname or partial name
        parts = en_name.split()
        if len(parts) >= 2:
            # Try last name match
            for pname, pdata in profiles_by_name.items():
                if parts[-1].lower() in pname:
                    profile = pdata
                    break

    if profile:
        matched += 1
        # Update fields if missing
        if not player.get('birth_date') and profile['birth_date']:
            player['birth_date'] = profile['birth_date']
            player['age'] = calc_age(profile['birth_date'])
            enriched += 1
        if not player.get('birth_place') and profile['birth_place']:
            player['birth_place'] = profile['birth_place']
        if not player.get('nationality') and profile['citizenship']:
            # citizenship can have multiple values separated by comma
            player['nationality'] = profile['citizenship']
        if not player.get('height') and profile['height']:
            player['height'] = f"{profile['height']} cm"
        if profile.get('foot'):
            player['foot'] = profile['foot']

        # Add national team stats if missing
        if en_name in nat_stats and not player.get('intl_goals'):
            ns = nat_stats[en_name]
            player['intl_goals'] = ns['intl_goals']
            player['intl_apps'] = ns['intl_apps']
            player['intl_assists'] = ns['intl_assists']

# Save
json.dump(details, open('player_details.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

with_age = sum(1 for p in details.values() if p.get('age'))
with_birth = sum(1 for p in details.values() if p.get('birth_date'))
with_place = sum(1 for p in details.values() if p.get('birth_place'))
with_intl = sum(1 for p in details.values() if p.get('intl_goals'))
with_club_stats = sum(1 for p in details.values() if p.get('club_goals'))

print(f"\n=== RESULTS ===")
print(f"Players in our DB: {len(details)}")
print(f"Matched to Transfermarkt: {matched}/{len(details)} ({100*matched//len(details)}%)")
print(f"Newly enriched (birth_date): {enriched}")
print(f"With birth_date: {with_birth} ({100*with_birth//len(details)}%)")
print(f"With birthplace: {with_place} ({100*with_place//len(details)}%)")
print(f"With age: {with_age} ({100*with_age//len(details)}%)")
print(f"With intl stats: {with_intl} ({100*with_intl//len(details)}%)")
print(f"With club stats: {with_club_stats}")
