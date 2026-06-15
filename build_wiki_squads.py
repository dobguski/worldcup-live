#!/usr/bin/env python3
"""
补充 Wikipedia/中文源完整球员名单数据
来源: 2026世界杯各队官方名单 (巴西/阿根廷/法国/德国/西班牙完整26人 + 其他队概要)
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# 完整26人名单 (from Chinese media / Wikipedia)
# ============================================================
WIKI_SQUADS = {
    "Argentina": {
        "coach": "利昂内尔·斯卡洛尼",
        "stadium": "Estadio Mâs Monumental",
        "players": [
            {"number": "1",  "name": "Juan Musso",           "name_cn": "胡安·穆索",                "position": "Goalkeeper",       "position_cn": "门将",   "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "12", "name": "Gerónimo Rulli",        "name_cn": "赫罗尼莫·鲁利",             "position": "Goalkeeper",       "position_cn": "门将",   "club": "Marseille",          "club_cn": "马赛"},
            {"number": "23", "name": "Emiliano Martínez",     "name_cn": "埃米利亚诺·马丁内斯",        "position": "Goalkeeper",       "position_cn": "门将",   "club": "Aston Villa",        "club_cn": "阿斯顿维拉"},
            {"number": "2",  "name": "Leonardo Balerdi",      "name_cn": "莱昂纳多·巴列尔迪",          "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Marseille",          "club_cn": "马赛"},
            {"number": "3",  "name": "Nicolás Tagliafico",    "name_cn": "尼古拉斯·塔利亚菲科",        "position": "Left-Back",        "position_cn": "左后卫",  "club": "Lyon",               "club_cn": "里昂"},
            {"number": "4",  "name": "Gonzalo Montiel",       "name_cn": "冈萨洛·蒙铁尔",             "position": "Right-Back",       "position_cn": "右后卫",  "club": "River Plate",        "club_cn": "河床"},
            {"number": "6",  "name": "Lisandro Martínez",     "name_cn": "利桑德罗·马丁内斯",          "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Manchester United",  "club_cn": "曼联"},
            {"number": "13", "name": "Cristian Romero",       "name_cn": "克里斯蒂安·罗梅罗",          "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Tottenham Hotspur",  "club_cn": "托特纳姆热刺"},
            {"number": "19", "name": "Nicolás Otamendi",      "name_cn": "尼古拉斯·奥塔门迪",          "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Benfica",            "club_cn": "本菲卡"},
            {"number": "25", "name": "Facundo Medina",        "name_cn": "法昆多·梅迪纳",             "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Marseille",          "club_cn": "马赛"},
            {"number": "26", "name": "Nahuel Molina",         "name_cn": "纳韦尔·莫利纳",             "position": "Right-Back",       "position_cn": "右后卫",  "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "5",  "name": "Leandro Paredes",       "name_cn": "莱安德罗·帕雷德斯",          "position": "Defensive Midfield","position_cn": "防守中场","club": "Boca Juniors",      "club_cn": "博卡青年"},
            {"number": "7",  "name": "Rodrigo De Paul",       "name_cn": "罗德里戈·德保罗",            "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Inter Miami",        "club_cn": "迈阿密国际"},
            {"number": "8",  "name": "Valentín Barco",        "name_cn": "瓦伦丁·巴尔科",             "position": "Left-Back",        "position_cn": "左后卫",  "club": "Strasbourg",         "club_cn": "斯特拉斯堡"},
            {"number": "11", "name": "Giovani Lo Celso",      "name_cn": "乔瓦尼·洛塞尔索",           "position": "Attacking Midfield","position_cn": "攻击中场","club": "Real Betis",         "club_cn": "皇家贝蒂斯"},
            {"number": "14", "name": "Exequiel Palacios",     "name_cn": "埃塞克尔·帕拉西奥斯",        "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Bayer Leverkusen",   "club_cn": "勒沃库森"},
            {"number": "20", "name": "Alexis Mac Allister",   "name_cn": "亚历克西斯·麦卡利斯特",       "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Liverpool",          "club_cn": "利物浦"},
            {"number": "24", "name": "Enzo Fernández",        "name_cn": "恩佐·费尔南德斯",            "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Chelsea",            "club_cn": "切尔西"},
            {"number": "9",  "name": "Julián Álvarez",        "name_cn": "胡利安·阿尔瓦雷斯",          "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "10", "name": "Lionel Messi",          "name_cn": "利昂内尔·梅西",             "position": "Forward",          "position_cn": "前锋",   "club": "Inter Miami",        "club_cn": "迈阿密国际"},
            {"number": "15", "name": "Nicolás González",      "name_cn": "尼古拉斯·冈萨雷斯",          "position": "Left Wing",        "position_cn": "左边锋",  "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "16", "name": "Thiago Almada",         "name_cn": "蒂亚戈·阿尔马达",            "position": "Attacking Midfield","position_cn": "攻击中场","club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "17", "name": "Giuliano Simeone",      "name_cn": "朱利亚诺·西蒙尼",            "position": "Forward",          "position_cn": "前锋",   "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "18", "name": "Nico Paz",              "name_cn": "尼科·帕斯",                 "position": "Attacking Midfield","position_cn": "攻击中场","club": "Como",               "club_cn": "科莫"},
            {"number": "21", "name": "José Manuel López",     "name_cn": "何塞·曼努埃尔·洛佩斯",       "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Palmeiras",          "club_cn": "帕尔梅拉斯"},
            {"number": "22", "name": "Lautaro Martínez",      "name_cn": "劳塔罗·马丁内斯",            "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Inter Milan",        "club_cn": "国际米兰"},
        ]
    },
    "Brazil": {
        "coach": "多里瓦尔·儒尼奥尔",
        "stadium": "Estádio do Maracanã",
        "players": [
            {"number": "1",  "name": "Alisson",               "name_cn": "阿利松",                   "position": "Goalkeeper",       "position_cn": "门将",   "club": "Liverpool",          "club_cn": "利物浦"},
            {"number": "12", "name": "Ederson",               "name_cn": "埃德松",                   "position": "Goalkeeper",       "position_cn": "门将",   "club": "Fenerbahçe",         "club_cn": "费内巴切"},
            {"number": "23", "name": "Weverton",              "name_cn": "韦弗顿",                   "position": "Goalkeeper",       "position_cn": "门将",   "club": "Grêmio",             "club_cn": "格雷米奥"},
            {"number": "2",  "name": "Alex Sandro",           "name_cn": "亚历克斯·桑德罗",           "position": "Left-Back",        "position_cn": "左后卫",  "club": "Flamengo",           "club_cn": "弗拉门戈"},
            {"number": "3",  "name": "Bremer",                "name_cn": "布雷默",                   "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Juventus",           "club_cn": "尤文图斯"},
            {"number": "4",  "name": "Danilo",                "name_cn": "达尼洛",                   "position": "Right-Back",       "position_cn": "右后卫",  "club": "Flamengo",           "club_cn": "弗拉门戈"},
            {"number": "6",  "name": "Douglas Santos",        "name_cn": "道格拉斯·桑托斯",           "position": "Left-Back",        "position_cn": "左后卫",  "club": "Zenit",              "club_cn": "泽尼特"},
            {"number": "13", "name": "Gabriel Magalhães",     "name_cn": "加布里埃尔·马加良斯",        "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "14", "name": "Ibañez",                "name_cn": "伊巴涅斯",                  "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Al-Ahli",            "club_cn": "吉达国民"},
            {"number": "15", "name": "Leo Pereira",           "name_cn": "莱奥·佩雷拉",               "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Flamengo",           "club_cn": "弗拉门戈"},
            {"number": "22", "name": "Marquinhos",            "name_cn": "马尔基尼奥斯",              "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "16", "name": "Wesley",                "name_cn": "韦斯利",                   "position": "Right-Back",       "position_cn": "右后卫",  "club": "Roma",               "club_cn": "罗马"},
            {"number": "5",  "name": "Bruno Guimarães",       "name_cn": "布鲁诺·吉马良斯",            "position": "Defensive Midfield","position_cn": "防守中场","club": "Newcastle United",   "club_cn": "纽卡斯尔联"},
            {"number": "8",  "name": "Casemiro",              "name_cn": "卡塞米罗",                  "position": "Defensive Midfield","position_cn": "防守中场","club": "Manchester United",  "club_cn": "曼联"},
            {"number": "17", "name": "Danilo Santos",         "name_cn": "达尼洛·桑托斯",             "position": "Midfielder",       "position_cn": "中场",   "club": "Botafogo",           "club_cn": "博塔弗戈"},
            {"number": "18", "name": "Fabinho",               "name_cn": "法比尼奥",                  "position": "Defensive Midfield","position_cn": "防守中场","club": "Al-Ittihad",        "club_cn": "吉达联合"},
            {"number": "20", "name": "Lucas Paquetá",         "name_cn": "卢卡斯·帕克塔",             "position": "Attacking Midfield","position_cn": "攻击中场","club": "Flamengo",           "club_cn": "弗拉门戈"},
            {"number": "7",  "name": "Endrick",               "name_cn": "恩德里克",                  "position": "Forward",          "position_cn": "前锋",   "club": "Lyon",               "club_cn": "里昂"},
            {"number": "9",  "name": "Gabriel Martinelli",    "name_cn": "马丁内利",                  "position": "Left Wing",        "position_cn": "左边锋",  "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "10", "name": "Neymar",                "name_cn": "内马尔",                   "position": "Forward",          "position_cn": "前锋",   "club": "Santos",             "club_cn": "桑托斯"},
            {"number": "11", "name": "Raphinha",              "name_cn": "拉菲尼亚",                  "position": "Right Winger",     "position_cn": "右边锋",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "19", "name": "Igor Thiago",           "name_cn": "伊戈尔·蒂亚戈",             "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Brentford",          "club_cn": "布伦特福德"},
            {"number": "21", "name": "Luiz Henrique",         "name_cn": "路易斯·恩里克",             "position": "Right Winger",     "position_cn": "右边锋",  "club": "Zenit",              "club_cn": "泽尼特"},
            {"number": "24", "name": "Matheus Cunha",         "name_cn": "马特乌斯·库尼亚",            "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Manchester United",  "club_cn": "曼联"},
            {"number": "25", "name": "Rayan",                 "name_cn": "拉扬",                     "position": "Forward",          "position_cn": "前锋",   "club": "Bournemouth",        "club_cn": "伯恩茅斯"},
            {"number": "26", "name": "Vinícius Júnior",       "name_cn": "维尼修斯·儒尼奥尔",          "position": "Left Wing",        "position_cn": "左边锋",  "club": "Real Madrid",        "club_cn": "皇家马德里"},
        ]
    },
    "France": {
        "coach": "迪迪埃·德尚",
        "stadium": "Stade de France",
        "players": [
            {"number": "16", "name": "Mike Maignan",          "name_cn": "迈尼昂",                   "position": "Goalkeeper",       "position_cn": "门将",   "club": "AC Milan",           "club_cn": "AC米兰"},
            {"number": "1",  "name": "Brice Samba",           "name_cn": "布莱斯·桑巴",              "position": "Goalkeeper",       "position_cn": "门将",   "club": "Rennes",             "club_cn": "雷恩"},
            {"number": "23", "name": "Lucas Chevalier",       "name_cn": "里塞",                     "position": "Goalkeeper",       "position_cn": "门将",   "club": "Lens",               "club_cn": "朗斯"},
            {"number": "4",  "name": "Dayot Upamecano",       "name_cn": "于帕梅卡诺",                "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "17", "name": "William Saliba",        "name_cn": "萨利巴",                   "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "15", "name": "Ibrahima Konaté",       "name_cn": "科纳特",                   "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Liverpool",          "club_cn": "利物浦"},
            {"number": "5",  "name": "Jules Koundé",          "name_cn": "孔德",                     "position": "Right-Back",       "position_cn": "右后卫",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "21", "name": "Lucas Hernández",       "name_cn": "卢卡斯·埃尔南德斯",         "position": "Left-Back",        "position_cn": "左后卫",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "3",  "name": "Lucas Digne",           "name_cn": "迪涅",                     "position": "Left-Back",        "position_cn": "左后卫",  "club": "Aston Villa",        "club_cn": "阿斯顿维拉"},
            {"number": "2",  "name": "Malo Gusto",            "name_cn": "古斯托",                   "position": "Right-Back",       "position_cn": "右后卫",  "club": "Chelsea",            "club_cn": "切尔西"},
            {"number": "19", "name": "Théo Hernández",        "name_cn": "特奥·埃尔南德斯",           "position": "Left-Back",        "position_cn": "左后卫",  "club": "Al-Hilal",           "club_cn": "利雅得新月"},
            {"number": "26", "name": "Maxence Lacroix",       "name_cn": "拉克鲁瓦",                  "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Crystal Palace",     "club_cn": "水晶宫"},
            {"number": "14", "name": "Adrien Rabiot",         "name_cn": "拉比奥",                   "position": "Central Midfield",  "position_cn": "中前卫",  "club": "AC Milan",           "club_cn": "AC米兰"},
            {"number": "8",  "name": "Aurélien Tchouaméni",   "name_cn": "楚阿梅尼",                  "position": "Defensive Midfield","position_cn": "防守中场","club": "Real Madrid",        "club_cn": "皇家马德里"},
            {"number": "13", "name": "N'Golo Kanté",          "name_cn": "坎特",                     "position": "Defensive Midfield","position_cn": "防守中场","club": "Fenerbahçe",         "club_cn": "费内巴切"},
            {"number": "6",  "name": "Manu Koné",             "name_cn": "夸迪奥·科内",              "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Roma",               "club_cn": "罗马"},
            {"number": "18", "name": "Warren Zaïre-Emery",    "name_cn": "扎伊尔·埃梅里",             "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "10", "name": "Kylian Mbappé",         "name_cn": "姆巴佩",                   "position": "Left Wing",        "position_cn": "左边锋",  "club": "Real Madrid",        "club_cn": "皇家马德里"},
            {"number": "7",  "name": "Ousmane Dembélé",       "name_cn": "登贝莱",                   "position": "Right Winger",     "position_cn": "右边锋",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "11", "name": "Michael Olise",         "name_cn": "奥利塞",                   "position": "Right Winger",     "position_cn": "右边锋",  "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "24", "name": "Rayan Cherki",          "name_cn": "谢尔基",                   "position": "Attacking Midfield","position_cn": "攻击中场","club": "Manchester City",    "club_cn": "曼城"},
            {"number": "20", "name": "Désiré Doué",           "name_cn": "杜埃",                     "position": "Attacking Midfield","position_cn": "攻击中场","club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "12", "name": "Bradley Barcola",       "name_cn": "巴尔科拉",                  "position": "Left Wing",        "position_cn": "左边锋",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "9",  "name": "Marcus Thuram",         "name_cn": "马库斯·图拉姆",             "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Inter Milan",        "club_cn": "国际米兰"},
            {"number": "25", "name": "Maghnes Akliouche",     "name_cn": "阿克利乌舍",                "position": "Attacking Midfield","position_cn": "攻击中场","club": "Monaco",             "club_cn": "摩纳哥"},
            {"number": "22", "name": "Jean-Philippe Mateta",   "name_cn": "马特塔",                   "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Crystal Palace",     "club_cn": "水晶宫"},
        ]
    },
    "Germany": {
        "coach": "尤利安·纳格尔斯曼",
        "stadium": "Olympiastadion Berlin",
        "players": [
            {"number": "1",  "name": "Oliver Baumann",        "name_cn": "奥利弗·鲍曼",              "position": "Goalkeeper",       "position_cn": "门将",   "club": "Hoffenheim",         "club_cn": "霍芬海姆"},
            {"number": "12", "name": "Manuel Neuer",          "name_cn": "曼努埃尔·诺伊尔",           "position": "Goalkeeper",       "position_cn": "门将",   "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "22", "name": "Alexander Nübel",       "name_cn": "亚历山大·努贝尔",           "position": "Goalkeeper",       "position_cn": "门将",   "club": "Stuttgart",          "club_cn": "斯图加特"},
            {"number": "2",  "name": "Waldemar Anton",        "name_cn": "瓦尔德马·安东",             "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Borussia Dortmund",  "club_cn": "多特蒙德"},
            {"number": "3",  "name": "Nathaniel Brown",       "name_cn": "纳撒尼尔·布朗",             "position": "Left-Back",        "position_cn": "左后卫",  "club": "Eintracht Frankfurt","club_cn": "法兰克福"},
            {"number": "4",  "name": "Pascal Groß",           "name_cn": "帕斯卡尔·格罗斯",           "position": "Defender",         "position_cn": "后卫",   "club": "Brighton and Hove Albion","club_cn":"布莱顿"},
            {"number": "5",  "name": "Joshua Kimmich",        "name_cn": "约书亚·基米希",             "position": "Right-Back",       "position_cn": "右后卫",  "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "6",  "name": "David Raum",            "name_cn": "大卫·劳姆",                "position": "Left-Back",        "position_cn": "左后卫",  "club": "RB Leipzig",         "club_cn": "RB莱比锡"},
            {"number": "15", "name": "Antonio Rüdiger",       "name_cn": "安东尼奥·吕迪格",           "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Real Madrid",        "club_cn": "皇家马德里"},
            {"number": "16", "name": "Nico Schlotterbeck",    "name_cn": "尼科·施洛特贝克",           "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Borussia Dortmund",  "club_cn": "多特蒙德"},
            {"number": "23", "name": "Jonathan Tah",          "name_cn": "约纳坦·塔",                "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "24", "name": "Malick Thiaw",          "name_cn": "马利克·蒂亚夫",             "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Newcastle United",   "club_cn": "纽卡斯尔联"},
            {"number": "8",  "name": "Aleksandar Pavlović",   "name_cn": "亚历山大·帕夫洛维奇",        "position": "Defensive Midfield","position_cn": "防守中场","club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "10", "name": "Jamal Musiala",         "name_cn": "贾马尔·穆西亚拉",           "position": "Attacking Midfield","position_cn": "攻击中场","club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "11", "name": "Nadiem Amiri",          "name_cn": "纳迪姆·阿米里",             "position": "Attacking Midfield","position_cn": "攻击中场","club": "Mainz",               "club_cn": "美因茨"},
            {"number": "13", "name": "Jamie Leweling",        "name_cn": "杰米·勒韦林",              "position": "Right Winger",     "position_cn": "右边锋",  "club": "Stuttgart",          "club_cn": "斯图加特"},
            {"number": "14", "name": "Felix Nmecha",          "name_cn": "费利克斯·恩梅查",           "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Borussia Dortmund",  "club_cn": "多特蒙德"},
            {"number": "17", "name": "Angelo Stiller",        "name_cn": "安杰洛·施蒂勒",             "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Stuttgart",          "club_cn": "斯图加特"},
            {"number": "18", "name": "Leon Goretzka",         "name_cn": "莱昂·格雷茨卡",             "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "19", "name": "Lennart Karl",          "name_cn": "伦纳特·卡尔",              "position": "Midfielder",       "position_cn": "中场",   "club": "Bayern Munich",      "club_cn": "拜仁慕尼黑"},
            {"number": "20", "name": "Florian Wirtz",         "name_cn": "弗洛里安·维尔茨",           "position": "Attacking Midfield","position_cn": "攻击中场","club": "Liverpool",          "club_cn": "利物浦"},
            {"number": "7",  "name": "Deniz Undav",           "name_cn": "德尼兹·翁达夫",             "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Stuttgart",          "club_cn": "斯图加特"},
            {"number": "9",  "name": "Kai Havertz",           "name_cn": "凯·哈弗茨",                "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "21", "name": "Maximilian Beier",      "name_cn": "马克西米利安·拜尔",          "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Borussia Dortmund",  "club_cn": "多特蒙德"},
            {"number": "25", "name": "Leroy Sané",            "name_cn": "勒鲁瓦·萨内",              "position": "Right Winger",     "position_cn": "右边锋",  "club": "Galatasaray",        "club_cn": "加拉塔萨雷"},
            {"number": "26", "name": "Nick Woltemade",        "name_cn": "尼克·沃尔特马德",           "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Newcastle United",   "club_cn": "纽卡斯尔联"},
        ]
    },
    "Spain": {
        "coach": "路易斯·德拉富恩特",
        "stadium": "Various",
        "players": [
            {"number": "1",  "name": "Unai Simón",            "name_cn": "乌奈·西蒙",                "position": "Goalkeeper",       "position_cn": "门将",   "club": "Athletic Bilbao",    "club_cn": "毕尔巴鄂竞技"},
            {"number": "13", "name": "David Raya",            "name_cn": "大卫·拉亚",                "position": "Goalkeeper",       "position_cn": "门将",   "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "23", "name": "Joan García",           "name_cn": "霍安·加西亚",              "position": "Goalkeeper",       "position_cn": "门将",   "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "2",  "name": "Marc Cucurella",        "name_cn": "库库雷利亚",                "position": "Left-Back",        "position_cn": "左后卫",  "club": "Chelsea",            "club_cn": "切尔西"},
            {"number": "3",  "name": "Alejandro Grimaldo",    "name_cn": "格里马尔多",                "position": "Left-Back",        "position_cn": "左后卫",  "club": "Bayer Leverkusen",   "club_cn": "勒沃库森"},
            {"number": "4",  "name": "Pau Cubarsí",           "name_cn": "库巴西",                   "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "5",  "name": "Aymeric Laporte",       "name_cn": "拉波尔特",                  "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Athletic Bilbao",    "club_cn": "毕尔巴鄂竞技"},
            {"number": "12", "name": "Eric García",           "name_cn": "埃里克·加西亚",             "position": "Centre-Back",      "position_cn": "中后卫",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "14", "name": "Marc Pubill",           "name_cn": "普维尔",                   "position": "Right-Back",       "position_cn": "右后卫",  "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "22", "name": "Pedro Porro",           "name_cn": "波罗",                     "position": "Right-Back",       "position_cn": "右后卫",  "club": "Tottenham Hotspur",  "club_cn": "托特纳姆热刺"},
            {"number": "25", "name": "Marcos Llorente",       "name_cn": "马科斯·略伦特",             "position": "Right-Back",       "position_cn": "右后卫",  "club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "6",  "name": "Pedri",                 "name_cn": "佩德里",                   "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "8",  "name": "Fabián Ruiz",           "name_cn": "法比安·鲁伊斯",             "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Paris SG",           "club_cn": "巴黎圣日耳曼"},
            {"number": "16", "name": "Martín Zubimendi",      "name_cn": "苏维门迪",                  "position": "Defensive Midfield","position_cn": "防守中场","club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "18", "name": "Gavi",                  "name_cn": "加维",                     "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "20", "name": "Rodri",                 "name_cn": "罗德里",                   "position": "Defensive Midfield","position_cn": "防守中场","club": "Manchester City",    "club_cn": "曼城"},
            {"number": "21", "name": "Álex Baena",            "name_cn": "巴埃纳",                   "position": "Attacking Midfield","position_cn": "攻击中场","club": "Atlético Madrid",    "club_cn": "马德里竞技"},
            {"number": "24", "name": "Mikel Merino",          "name_cn": "梅里诺",                   "position": "Central Midfield",  "position_cn": "中前卫",  "club": "Arsenal",            "club_cn": "阿森纳"},
            {"number": "7",  "name": "Lamine Yamal",          "name_cn": "拉明·亚马尔",              "position": "Right Winger",     "position_cn": "右边锋",  "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "9",  "name": "Mikel Oyarzabal",       "name_cn": "奥亚萨瓦尔",                "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Real Sociedad",      "club_cn": "皇家社会"},
            {"number": "10", "name": "Dani Olmo",             "name_cn": "奥尔莫",                   "position": "Attacking Midfield","position_cn": "攻击中场","club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "11", "name": "Nico Williams",         "name_cn": "尼科·威廉姆斯",             "position": "Left Wing",        "position_cn": "左边锋",  "club": "Athletic Bilbao",    "club_cn": "毕尔巴鄂竞技"},
            {"number": "15", "name": "Yéremy Pino",           "name_cn": "皮诺",                     "position": "Right Winger",     "position_cn": "右边锋",  "club": "Crystal Palace",     "club_cn": "水晶宫"},
            {"number": "17", "name": "Ferran Torres",         "name_cn": "费兰·托雷斯",              "position": "Forward",          "position_cn": "前锋",   "club": "Barcelona",          "club_cn": "巴塞罗那"},
            {"number": "19", "name": "Borja Iglesias",        "name_cn": "伊格莱西亚斯",              "position": "Centre-Forward",    "position_cn": "中锋",   "club": "Celta Vigo",         "club_cn": "塞尔塔"},
            {"number": "26", "name": "Iker Muñoz",            "name_cn": "穆尼奥斯",                  "position": "Midfielder",       "position_cn": "中场",   "club": "Osasuna",            "club_cn": "奥萨苏纳"},
        ]
    },
}

# ============================================================
# MERGE
# ============================================================
def merge():
    base = json.load(open('teams.json', encoding='utf-8'))

    for team_name, wiki_data in WIKI_SQUADS.items():
        if team_name not in base:
            print(f"  SKIP {team_name}: not in GROUPS")
            continue

        old_count = len(base[team_name].get('players', []))
        base[team_name]['players'] = wiki_data['players']
        if wiki_data.get('coach'):
            base[team_name]['coach'] = wiki_data['coach']
        if wiki_data.get('stadium'):
            base[team_name]['stadium'] = wiki_data['stadium']
        print(f"  {team_name}: {old_count} -> {len(wiki_data['players'])} players")

    total = sum(len(t['players']) for t in base.values())
    cn_names = sum(1 for t in base.values() for p in t['players'] if p.get('name_cn'))
    cn_pos = sum(1 for t in base.values() for p in t['players'] if p.get('position_cn'))
    cn_club = sum(1 for t in base.values() for p in t['players'] if p.get('club_cn'))

    print(f"\n  Total: {total} players across {len(base)} teams")
    print(f"  CN names: {cn_names}/{total} ({100*cn_names//total}%)")
    print(f"  CN positions: {cn_pos}/{total} ({100*cn_pos//total}%)")
    print(f"  CN clubs: {cn_club}/{total} ({100*cn_club//total}%)")

    json.dump(base, open('teams.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"\n  Saved teams.json")

if __name__ == '__main__':
    merge()
