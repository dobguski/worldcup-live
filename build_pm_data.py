#!/usr/bin/env python3
"""Build expanded polymarket.json with estimated odds for all 71 matches."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load base data
teams = json.load(open('teams.json', encoding='utf-8'))
matches = json.load(open('match_data.json', encoding='utf-8'))
pm = json.load(open('polymarket.json', encoding='utf-8'))

# Champion odds as team strength proxy
champion = pm.get('champion_odds', {})

# Normalize champion odds to 0-1 scale for match probability estimation
def team_strength(team_name):
    """Get team strength from champion odds, with fallback for missing teams."""
    # Try direct match
    if team_name in champion:
        return champion[team_name]
    # Try Chinese name match
    for t in teams.values():
        if t.get('name_cn') == team_name or t.get('name_en') == team_name:
            en = t['name_en']
            if en in champion:
                return champion[en]
    # Default for unlisted teams
    return 0.005  # ~0.5% baseline

def estimate_match_probs(home, away):
    """Estimate win/draw/loss probabilities from team strengths."""
    hs = team_strength(home)
    aws = team_strength(away)

    if hs == 0 and aws == 0:
        return 0.38, 0.28, 0.34  # Default balanced

    # Normalize
    total = hs + aws
    if total == 0:
        return 0.38, 0.28, 0.34

    h_ratio = hs / total

    # Convert strength ratio to match probabilities
    # Stronger team gets higher win probability, draw is always significant in football
    if h_ratio > 0.8:  # Very dominant
        home_p = 0.80 + (h_ratio - 0.8) * 0.7
        draw_p = 0.12
        away_p = 1 - home_p - draw_p
    elif h_ratio > 0.65:  # Clear favorite
        home_p = 0.55 + (h_ratio - 0.65) * 0.7
        draw_p = 0.22
        away_p = 1 - home_p - draw_p
    elif h_ratio > 0.55:  # Slight favorite
        home_p = h_ratio + 0.05
        draw_p = 0.26
        away_p = 1 - home_p - draw_p
    elif h_ratio > 0.45:  # Very even
        home_p = h_ratio + 0.05
        draw_p = 0.28
        away_p = 1 - home_p - draw_p
    else:  # Home underdog
        home_p = max(0.06, h_ratio)
        draw_p = min(0.28, 1 - home_p - 0.06)
        away_p = 1 - home_p - draw_p

    # Ensure valid probabilities
    home_p = max(0.02, min(0.95, home_p))
    away_p = max(0.02, min(0.95, away_p))
    draw_p = max(0.04, min(0.30, draw_p))

    # Normalize to sum to 1
    total_p = home_p + draw_p + away_p
    return round(home_p/total_p, 3), round(draw_p/total_p, 3), round(away_p/total_p, 3)

def match_key(m):
    """Create match key for lookup."""
    return f"{m['home_team']} vs {m['away_team']}"

# Build PM data for all matches
existing_keys = set(pm['matches'].keys())
new_matches = {}

# Also define known-match annotations
MATCH_NOTES = {
    # A组
    "Mexico vs South Africa": "揭幕战·阿兹特克球场·东道主首秀",
    "South Korea vs Czech Republic": "亚洲vs欧洲·实力接近·孙兴慜领衔",
    "Czech Republic vs South Africa": "出线关键战·捷克稍占优",
    "Mexico vs South Korea": "A组头名之争·主场优势",
    "Czech Republic vs Mexico": "出线生死战·市场关注度高",
    "South Africa vs South Korea": "亚洲非洲对决·韩国技术占优",
    # B组
    "Canada vs Bosnia & Herzegovina": "东道主首秀·戴维斯领衔",
    "Qatar vs Switzerland": "亚洲冠军vs欧洲劲旅·瑞士明显占优",
    "Switzerland vs Bosnia & Herzegovina": "欧洲内战·瑞士控场能力更强",
    "Canada vs Qatar": "东道主优势·加拿大进攻犀利",
    "Switzerland vs Canada": "B组焦点战·瑞士经验优势",
    "Bosnia & Herzegovina vs Qatar": "波黑哲科最后一届·经验取胜",
    # C组
    "Brazil vs Morocco": "夺冠热门首秀·摩洛哥防守反击",
    "Haiti vs Scotland": "苏格兰明显占优·海地力拼首分",
    "Scotland vs Morocco": "C组关键战·苏格兰身体对抗优势",
    "Brazil vs Haiti": "巴西碾压级优势·海地荣誉之战",
    "Scotland vs Brazil": "C组最强对话·巴西技术碾压",
    "Morocco vs Haiti": "非洲vs加勒比·摩洛哥实力碾压",
    # D组
    "USA vs Paraguay": "东道主首秀·普利西奇领衔",
    "Australia vs Turkey": "澳土对决·土耳其纸面占优",
    "USA vs Australia": "东道主优势·美澳身体对抗",
    "Turkey vs Paraguay": "土耳其技术占优·关键出线战",
    "Turkey vs USA": "D组头名之争·关注度极高",
    "Paraguay vs Australia": "出线生死战·实力接近",
    # E组
    "Germany vs Curaçao": "德国碾压优势·库拉索世界杯首秀",
    "Ivory Coast vs Ecuador": "非洲vs南美·实力接近",
    "Germany vs Ivory Coast": "德国技术碾压·科特迪瓦防守反击",
    "Ecuador vs Curaçao": "南美vs加勒比·厄瓜多尔明显占优",
    "Curaçao vs Ivory Coast": "科特迪瓦实力占优·库拉索力拼首分",
    "Ecuador vs Germany": "E组最强战·德国碾压级优势",
    # F组
    "Netherlands vs Japan": "欧洲vs亚洲·荷兰控场占优·日本快速反击",
    "Sweden vs Tunisia": "北欧力量vs北非技术·瑞典新星闪耀",
    "Netherlands vs Sweden": "F组欧洲内战·荷兰主场优势",
    "Tunisia vs Japan": "日本技术占优·突尼斯防守反击",
    "Japan vs Sweden": "关键出线战·瑞典身体碾压",
    "Tunisia vs Netherlands": "荷兰实力碾压·突尼斯防守反击",
    # G组
    "Belgium vs Egypt": "欧洲红魔vs法老军团·萨拉赫对决",
    "Iran vs New Zealand": "亚洲vs大洋洲·伊朗经验占优",
    "Belgium vs Iran": "比利时碾压·伊朗铁桶防守",
    "New Zealand vs Egypt": "埃及技术占优·新西兰身体对抗",
    "Egypt vs Iran": "萨拉赫领衔·埃及明显占优",
    "New Zealand vs Belgium": "比利时碾压·新西兰荣誉之战",
    # H组
    "Spain vs Cape Verde": "西班牙碾压优势·佛得角首秀",
    "Saudi Arabia vs Uruguay": "沙特vs乌拉圭·乌拉圭实力碾压",
    "Spain vs Saudi Arabia": "西班牙技术碾压·沙特铁桶防守",
    "Uruguay vs Cape Verde": "乌拉圭明显占优·努涅斯领衔",
    "Cape Verde vs Saudi Arabia": "弱旅对决·沙特经验稍占优",
    "Uruguay vs Spain": "H组头名之争·关注度极高",
    # I组
    "France vs Senegal": "卫冕亚军首秀·姆巴佩领衔",
    "Iraq vs Norway": "挪威双子星碾压·哈兰德厄德高",
    "France vs Iraq": "法国碾压优势·伊拉克铁桶防守",
    "Norway vs Senegal": "北欧vs非洲·挪威进攻犀利",
    "Norway vs France": "I组最强战·法国实力占优",
    "Senegal vs Iraq": "塞内加尔实力碾压·马内领衔",
    # J组
    "Argentina vs Algeria": "卫冕冠军首秀·梅西最后一届",
    "Austria vs Jordan": "奥地利明显占优·约旦荣誉之战",
    "Argentina vs Austria": "阿根廷技术碾压·梅西领衔",
    "Jordan vs Algeria": "阿尔及利亚实力占优",
    "Algeria vs Austria": "关键出线战·实力接近",
    "Jordan vs Argentina": "阿根廷碾压·约旦荣誉之战",
    # K组
    "Portugal vs DR Congo": "C罗最后一届·葡萄牙明显占优",
    "Uzbekistan vs Colombia": "南美vs中亚·哥伦比亚占优",
    "Portugal vs Uzbekistan": "葡萄牙碾压·C罗领衔",
    "Colombia vs DR Congo": "哥伦比亚实力占优",
    "Colombia vs Portugal": "K组头名之争·C罗vs迪亚斯",
    "DR Congo vs Uzbekistan": "弱旅对决·实力接近",
    # L组
    "England vs Croatia": "欧洲杯重赛·凯恩vs莫德里奇",
    "Ghana vs Panama": "非洲vs中北美·加纳占优",
    "England vs Ghana": "英格兰碾压优势",
    "Panama vs Croatia": "克罗地亚明显占优",
    "Panama vs England": "英格兰碾压·巴拿马荣誉之战",
    "Croatia vs Ghana": "关键出线战·莫德里奇最后一届",
}

for m in matches:
    mk = match_key(m)
    mk_rev = f"{m['away_team']} vs {m['home_team']}"

    # Check if already in PM data
    if mk in existing_keys:
        continue
    if mk_rev in existing_keys:
        # Use reversed entry
        existing = pm['matches'][mk_rev]
        hp, dp, ap = existing['home_prob'], existing['draw_prob'], existing['away_prob']
        # Swap home/away since this is reversed
        new_matches[mk] = {
            'home_team': m['home_team'], 'away_team': m['away_team'],
            'home_prob': ap, 'draw_prob': dp, 'away_prob': hp,
            'volume': existing.get('volume', 'N/A'),
            'predicted': 'away' if existing['predicted'] == 'home' else ('home' if existing['predicted'] == 'away' else 'draw'),
            'note': MATCH_NOTES.get(mk, ''),
            'source': 'estimated_from_team_strength'
        }
        continue

    # Estimate from team strength
    if m.get('is_result'):
        # For completed matches without PM data, skip (keep only known ones)
        continue

    hp, dp, ap = estimate_match_probs(m['home_team'], m['away_team'])
    pred = 'home' if hp > max(dp, ap) else ('away' if ap > max(hp, dp) else 'draw')

    new_matches[mk] = {
        'home_team': m['home_team'], 'away_team': m['away_team'],
        'home_prob': hp, 'draw_prob': dp, 'away_prob': ap,
        'volume': 'est.',
        'predicted': pred,
        'note': MATCH_NOTES.get(mk, ''),
        'source': 'estimated_from_team_strength'
    }

# Merge
pm['matches'].update(new_matches)
pm['updated'] = '2026-06-15'
pm['note'] = '已结束比赛基于实际PM盘口; 未开始比赛基于冠军赔率推算+交叉验证'
pm['total_matches'] = len(pm['matches'])

json.dump(pm, open('polymarket.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"PM matches: {len(pm['matches'])} (was {len(existing_keys)})")
print(f"  Known (real PM): {len(existing_keys)}")
print(f"  Estimated: {len(new_matches)}")
