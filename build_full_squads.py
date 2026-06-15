#!/usr/bin/env python3
"""Build complete wiki_squads.json from web search data for all 48 teams."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

S = {}  # shorthand for squad data

# ===== A组 =====
S["South Korea"] = {"coach": "洪明甫", "players": [
    {"number":"1","name":"Kim Seung-gyu","name_cn":"金承奎","position":"Goalkeeper","position_cn":"门将","club":"FC Tokyo","club_cn":"FC东京"},
    {"number":"12","name":"Song Bum-keun","name_cn":"宋范根","position":"Goalkeeper","position_cn":"门将","club":"Jeonbuk Hyundai","club_cn":"全北现代"},
    {"number":"21","name":"Jo Hyeon-woo","name_cn":"赵贤祐","position":"Goalkeeper","position_cn":"门将","club":"Ulsan HD","club_cn":"蔚山HD"},
    {"number":"2","name":"Lee Han-beom","name_cn":"李韩汎","position":"Centre-Back","position_cn":"中后卫","club":"FC Midtjylland","club_cn":"中日德兰"},
    {"number":"4","name":"Kim Min-jae","name_cn":"金玟哉","position":"Centre-Back","position_cn":"中后卫","club":"Bayern Munich","club_cn":"拜仁慕尼黑"},
    {"number":"5","name":"Kim Tae-hyeon","name_cn":"金太铉","position":"Defender","position_cn":"后卫","club":"Kashima Antlers","club_cn":"鹿岛鹿角"},
    {"number":"14","name":"Cho Wi-je","name_cn":"赵伟济","position":"Defender","position_cn":"后卫","club":"Jeonbuk Hyundai","club_cn":"全北现代"},
    {"number":"15","name":"Kim Moon-hwan","name_cn":"金纹焕","position":"Right-Back","position_cn":"右后卫","club":"Daejeon Hana","club_cn":"大田韩亚"},
    {"number":"22","name":"Seol Young-woo","name_cn":"薛英佑","position":"Left-Back","position_cn":"左后卫","club":"Red Star Belgrade","club_cn":"贝尔格莱德红星"},
    {"number":"23","name":"Jens Castrop","name_cn":"延斯·卡斯特罗普","position":"Defender","position_cn":"后卫","club":"Borussia Mönchengladbach","club_cn":"门兴"},
    {"number":"3","name":"Lee Ki-hyuk","name_cn":"李期奕","position":"Defender","position_cn":"后卫","club":"Gangwon FC","club_cn":"江原FC"},
    {"number":"13","name":"Lee Tae-seok","name_cn":"李太锡","position":"Defender","position_cn":"后卫","club":"Austria Wien","club_cn":"奥地利维也纳"},
    {"number":"6","name":"Hwang In-beom","name_cn":"黄仁范","position":"Central Midfield","position_cn":"中前卫","club":"Feyenoord","club_cn":"费耶诺德"},
    {"number":"8","name":"Paik Seung-ho","name_cn":"白昇浩","position":"Midfielder","position_cn":"中场","club":"Birmingham City","club_cn":"伯明翰城"},
    {"number":"10","name":"Lee Jae-sung","name_cn":"李在城","position":"Midfielder","position_cn":"中场","club":"Mainz","club_cn":"美因茨"},
    {"number":"11","name":"Hwang Hee-chan","name_cn":"黄喜灿","position":"Left Wing","position_cn":"左边锋","club":"Wolves","club_cn":"狼队"},
    {"number":"16","name":"Park Jin-seop","name_cn":"朴镇燮","position":"Midfielder","position_cn":"中场","club":"Zhejiang FC","club_cn":"浙江FC"},
    {"number":"17","name":"Bae Jun-ho","name_cn":"裴俊浩","position":"Midfielder","position_cn":"中场","club":"Stoke City","club_cn":"斯托克城"},
    {"number":"19","name":"Lee Kang-in","name_cn":"李刚仁","position":"Attacking Midfield","position_cn":"攻击中场","club":"Paris SG","club_cn":"巴黎圣日耳曼"},
    {"number":"20","name":"Yang Hyun-jun","name_cn":"杨贤俊","position":"Winger","position_cn":"边锋","club":"Celtic","club_cn":"凯尔特人"},
    {"number":"24","name":"Kim Jin-gyu","name_cn":"金镇圭","position":"Midfielder","position_cn":"中场","club":"Jeonbuk Hyundai","club_cn":"全北现代"},
    {"number":"25","name":"Eom Ji-sung","name_cn":"严智星","position":"Winger","position_cn":"边锋","club":"Swansea City","club_cn":"斯旺西城"},
    {"number":"26","name":"Lee Dong-gyeong","name_cn":"李东炅","position":"Midfielder","position_cn":"中场","club":"Ulsan HD","club_cn":"蔚山HD"},
    {"number":"7","name":"Son Heung-min","name_cn":"孙兴慜","position":"Left Wing","position_cn":"左边锋","club":"Los Angeles FC","club_cn":"洛杉矶FC"},
    {"number":"9","name":"Cho Gue-sung","name_cn":"曹圭成","position":"Centre-Forward","position_cn":"中锋","club":"FC Midtjylland","club_cn":"中日德兰"},
    {"number":"18","name":"Oh Hyeon-gyu","name_cn":"吴贤揆","position":"Centre-Forward","position_cn":"中锋","club":"Beşiktaş","club_cn":"贝西克塔斯"},
]}

S["Mexico"] = {"coach": "哈维尔·阿吉雷", "players": [
    {"number":"1","name":"Guillermo Ochoa","name_cn":"吉列尔莫·奥乔亚","position":"Goalkeeper","position_cn":"门将","club":"AEL Limassol","club_cn":"AEL利马索尔"},
    {"number":"12","name":"José Rangel","name_cn":"何塞·兰格尔","position":"Goalkeeper","position_cn":"门将","club":"CD Guadalajara","club_cn":"瓜达拉哈拉"},
    {"number":"23","name":"Carlos Acevedo","name_cn":"卡洛斯·阿切维多","position":"Goalkeeper","position_cn":"门将","club":"Santos Laguna","club_cn":"桑托斯拉古纳"},
    {"number":"2","name":"Jorge Sánchez","name_cn":"豪尔赫·桑切斯","position":"Right-Back","position_cn":"右后卫","club":"PAOK","club_cn":"塞萨洛尼基"},
    {"number":"3","name":"César Montes","name_cn":"塞萨尔·蒙特斯","position":"Centre-Back","position_cn":"中后卫","club":"Lokomotiv Moscow","club_cn":"莫斯科火车头"},
    {"number":"4","name":"Johan Vásquez","name_cn":"约翰·巴斯克斯","position":"Centre-Back","position_cn":"中后卫","club":"Genoa","club_cn":"热那亚"},
    {"number":"5","name":"Jesús Gallardo","name_cn":"赫苏斯·加利亚多","position":"Left-Back","position_cn":"左后卫","club":"Toluca","club_cn":"托卢卡"},
    {"number":"13","name":"Israel Reyes","name_cn":"伊塞尔·雷耶斯","position":"Defender","position_cn":"后卫","club":"Club América","club_cn":"美洲队"},
    {"number":"16","name":"Mateo Chávez","name_cn":"马特奥·查韦斯","position":"Left-Back","position_cn":"左后卫","club":"AZ Alkmaar","club_cn":"阿尔克马尔"},
    {"number":"6","name":"Edson Álvarez","name_cn":"埃德森·阿尔瓦雷斯","position":"Defensive Midfield","position_cn":"防守中场","club":"Fenerbahçe","club_cn":"费内巴切"},
    {"number":"7","name":"Luis Romo","name_cn":"路易斯·罗莫","position":"Central Midfield","position_cn":"中前卫","club":"CD Guadalajara","club_cn":"瓜达拉哈拉"},
    {"number":"8","name":"Álvaro Fidalgo","name_cn":"阿尔瓦罗·菲达尔戈","position":"Central Midfield","position_cn":"中前卫","club":"Real Betis","club_cn":"皇家贝蒂斯"},
    {"number":"14","name":"Brian Gutiérrez","name_cn":"布莱恩·古铁雷斯","position":"Midfielder","position_cn":"中场","club":"CD Guadalajara","club_cn":"瓜达拉哈拉"},
    {"number":"15","name":"Obed Vargas","name_cn":"奥贝德·巴尔加斯","position":"Midfielder","position_cn":"中场","club":"Atlético Madrid","club_cn":"马德里竞技"},
    {"number":"18","name":"Luis Chávez","name_cn":"路易斯·查韦斯","position":"Central Midfield","position_cn":"中前卫","club":"Dynamo Moscow","club_cn":"莫斯科迪纳摩"},
    {"number":"20","name":"Erik Lira","name_cn":"埃里克·里拉","position":"Defensive Midfield","position_cn":"防守中场","club":"Cruz Azul","club_cn":"蓝十字"},
    {"number":"21","name":"Gilberto Mora","name_cn":"希尔韦托·莫拉","position":"Midfielder","position_cn":"中场","club":"Tijuana","club_cn":"蒂华纳"},
    {"number":"24","name":"Orbelín Pineda","name_cn":"皮内达","position":"Midfielder","position_cn":"中场","club":"AEK Athens","club_cn":"雅典AEK"},
    {"number":"9","name":"Santiago Giménez","name_cn":"圣地亚哥·希门尼斯","position":"Centre-Forward","position_cn":"中锋","club":"AC Milan","club_cn":"AC米兰"},
    {"number":"10","name":"Raúl Jiménez","name_cn":"劳尔·希门尼斯","position":"Centre-Forward","position_cn":"中锋","club":"Fulham","club_cn":"富勒姆"},
    {"number":"11","name":"Alexis Vega","name_cn":"阿莱克斯·维加","position":"Left Wing","position_cn":"左边锋","club":"Toluca","club_cn":"托卢卡"},
    {"number":"17","name":"Roberto Alvarado","name_cn":"罗伯托·阿尔瓦拉多","position":"Winger","position_cn":"边锋","club":"CD Guadalajara","club_cn":"瓜达拉哈拉"},
    {"number":"19","name":"César Huerta","name_cn":"塞萨尔·韦尔塔","position":"Winger","position_cn":"边锋","club":"Anderlecht","club_cn":"安德莱赫特"},
    {"number":"22","name":"Armando González","name_cn":"阿曼多·冈萨雷斯","position":"Forward","position_cn":"前锋","club":"CD Guadalajara","club_cn":"瓜达拉哈拉"},
    {"number":"25","name":"Guillermo Martínez","name_cn":"吉列尔莫·马丁内斯","position":"Centre-Forward","position_cn":"中锋","club":"Pumas","club_cn":"美洲狮"},
    {"number":"26","name":"Julián Quiñones","name_cn":"奎尼奥内斯","position":"Forward","position_cn":"前锋","club":"Al-Qadsiah","club_cn":"胡拜尔库迪西亚"},
]}

S["Czech Republic"] = {"coach": "伊万·哈谢克", "players": [
    {"number":"1","name":"Matěj Kovář","name_cn":"马泰·科瓦日","position":"Goalkeeper","position_cn":"门将","club":"PSV Eindhoven","club_cn":"PSV埃因霍温"},
    {"number":"16","name":"Jindřich Staněk","name_cn":"因德里奇·斯塔涅克","position":"Goalkeeper","position_cn":"门将","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"23","name":"Lukáš Horníček","name_cn":"卢卡斯·霍尔尼切克","position":"Goalkeeper","position_cn":"门将","club":"Braga","club_cn":"布拉加"},
    {"number":"2","name":"David Zima","name_cn":"大卫·齐马","position":"Centre-Back","position_cn":"中后卫","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"3","name":"Tomáš Holeš","name_cn":"托马斯·霍莱什","position":"Centre-Back","position_cn":"中后卫","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"4","name":"Robin Hranáč","name_cn":"罗宾·赫拉纳奇","position":"Centre-Back","position_cn":"中后卫","club":"Hoffenheim","club_cn":"霍芬海姆"},
    {"number":"5","name":"Vladimír Coufal","name_cn":"弗拉基米尔·曹法尔","position":"Right-Back","position_cn":"右后卫","club":"Hoffenheim","club_cn":"霍芬海姆"},
    {"number":"7","name":"Ladislav Krejčí","name_cn":"拉迪斯拉夫·克雷伊奇","position":"Centre-Back","position_cn":"中后卫","club":"Wolves","club_cn":"狼队"},
    {"number":"14","name":"David Jurásek","name_cn":"大卫·尤拉塞克","position":"Left-Back","position_cn":"左后卫","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"20","name":"Jaroslav Zelený","name_cn":"雅罗斯拉夫·泽勒尼","position":"Left-Back","position_cn":"左后卫","club":"Sparta Prague","club_cn":"布拉格斯巴达"},
    {"number":"8","name":"Vladimír Darida","name_cn":"弗拉基米尔·达里达","position":"Central Midfield","position_cn":"中前卫","club":"Hradec Králové","club_cn":"赫拉德茨克拉洛韦"},
    {"number":"15","name":"Pavel Šulc","name_cn":"帕维尔·舒尔茨","position":"Attacking Midfield","position_cn":"攻击中场","club":"Lyon","club_cn":"里昂"},
    {"number":"17","name":"Lukáš Provod","name_cn":"卢卡斯·普罗沃德","position":"Midfielder","position_cn":"中场","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"18","name":"Michal Sadílek","name_cn":"米哈尔·萨迪莱克","position":"Midfielder","position_cn":"中场","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"22","name":"Tomáš Souček","name_cn":"托马斯·绍切克","position":"Central Midfield","position_cn":"中前卫","club":"West Ham United","club_cn":"西汉姆联"},
    {"number":"12","name":"Lukáš Červ","name_cn":"卢卡斯·切尔夫","position":"Midfielder","position_cn":"中场","club":"Viktoria Plzeň","club_cn":"比尔森胜利"},
    {"number":"6","name":"Štěpán Chaloupek","name_cn":"什捷潘·哈劳佩克","position":"Defender","position_cn":"后卫","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"21","name":"David Douděra","name_cn":"大卫·道杰拉","position":"Defender","position_cn":"后卫","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"9","name":"Adam Hložek","name_cn":"亚当·赫洛热克","position":"Forward","position_cn":"前锋","club":"Hoffenheim","club_cn":"霍芬海姆"},
    {"number":"10","name":"Patrik Schick","name_cn":"帕特里克·希克","position":"Centre-Forward","position_cn":"中锋","club":"Bayer Leverkusen","club_cn":"勒沃库森"},
    {"number":"11","name":"Jan Kuchta","name_cn":"扬·库赫塔","position":"Centre-Forward","position_cn":"中锋","club":"Sparta Prague","club_cn":"布拉格斯巴达"},
    {"number":"13","name":"Mojmír Chytil","name_cn":"莫伊米尔·希季尔","position":"Forward","position_cn":"前锋","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"19","name":"Tomáš Chorý","name_cn":"托马什·绍里","position":"Centre-Forward","position_cn":"中锋","club":"Slavia Prague","club_cn":"布拉格斯拉维亚"},
    {"number":"25","name":"Hugo Schuhurek","name_cn":"乌戈·索胡雷克","position":"Midfielder","position_cn":"中场","club":"Sparta Prague","club_cn":"布拉格斯巴达"},
    {"number":"24","name":"Alexandr Sojka","name_cn":"亚历山大·索伊卡","position":"Midfielder","position_cn":"中场","club":"Viktoria Plzeň","club_cn":"比尔森胜利"},
    {"number":"26","name":"Denis Višinský","name_cn":"丹尼斯·维辛斯基","position":"Midfielder","position_cn":"中场","club":"Viktoria Plzeň","club_cn":"比尔森胜利"},
]}

S["South Africa"] = {"coach": "雨果·布鲁斯", "players": [
    {"number":"1","name":"Ronwen Williams","name_cn":"罗恩文·威廉姆斯","position":"Goalkeeper","position_cn":"门将","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"16","name":"Ricardo Goss","name_cn":"里卡多·戈斯","position":"Goalkeeper","position_cn":"门将","club":"SuperSport United","club_cn":"西韦莱莱"},
    {"number":"23","name":"Sipho Chaine","name_cn":"西波·钱恩","position":"Goalkeeper","position_cn":"门将","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"2","name":"Kuliso Mudau","name_cn":"库利索·穆达乌","position":"Right-Back","position_cn":"右后卫","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"3","name":"Nkosinathi Sibisi","name_cn":"恩科西纳蒂·西比西","position":"Centre-Back","position_cn":"中后卫","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"4","name":"Ime Okon","name_cn":"伊梅·奥孔","position":"Centre-Back","position_cn":"中后卫","club":"Hannover 96","club_cn":"汉诺威96"},
    {"number":"5","name":"Kulumani Ndamane","name_cn":"库卢马尼·恩达马内","position":"Centre-Back","position_cn":"中后卫","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"6","name":"Aubrey Modiba","name_cn":"奥布雷·莫迪巴","position":"Left-Back","position_cn":"左后卫","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"13","name":"Thabang Matuludi","name_cn":"塔邦·马图鲁迪","position":"Defender","position_cn":"后卫","club":"Polokwane City","club_cn":"波洛夸内城"},
    {"number":"14","name":"Samukelo Kabini","name_cn":"萨穆凯洛·卡比尼","position":"Defender","position_cn":"后卫","club":"Molde FK","club_cn":"莫尔德"},
    {"number":"15","name":"Olwethu Makhanya","name_cn":"奥尔韦图·马卡尼亚","position":"Defender","position_cn":"后卫","club":"Philadelphia Union","club_cn":"费城联合"},
    {"number":"19","name":"Bradley Cross","name_cn":"布拉德利·克罗斯","position":"Centre-Back","position_cn":"中后卫","club":"Kaizer Chiefs","club_cn":"凯撒酋长"},
    {"number":"22","name":"Kamogelo Sebelebele","name_cn":"卡莫盖洛·塞贝莱贝莱","position":"Defender","position_cn":"后卫","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"7","name":"Teboho Mokoena","name_cn":"泰博霍·莫科纳","position":"Central Midfield","position_cn":"中前卫","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"8","name":"Talent Mbatha","name_cn":"塔伦特·姆巴塔","position":"Midfielder","position_cn":"中场","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"12","name":"Sphephelo Sithole","name_cn":"斯皮菲洛·西索莱","position":"Midfielder","position_cn":"中场","club":"CD Tondela","club_cn":"CD通德拉"},
    {"number":"20","name":"Jayden Adams","name_cn":"杰登·亚当斯","position":"Midfielder","position_cn":"中场","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"9","name":"Lyle Foster","name_cn":"莱尔·福斯特","position":"Centre-Forward","position_cn":"中锋","club":"Burnley","club_cn":"伯恩利"},
    {"number":"10","name":"Oswin Appollis","name_cn":"奥斯温·阿波利斯","position":"Winger","position_cn":"边锋","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"11","name":"Iqraam Rayners","name_cn":"伊克拉姆·雷纳斯","position":"Forward","position_cn":"前锋","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"17","name":"Evidence Makgopa","name_cn":"埃维登斯·马科戈帕","position":"Centre-Forward","position_cn":"中锋","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"18","name":"Relebohile Mofokeng","name_cn":"雷莱博希莱·莫福肯","position":"Winger","position_cn":"边锋","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"21","name":"Themba Zwane","name_cn":"滕巴·兹瓦内","position":"Attacking Midfield","position_cn":"攻击中场","club":"Mamelodi Sundowns","club_cn":"马梅洛迪日落"},
    {"number":"24","name":"Thapelo Maseko","name_cn":"塔佩洛·马塞科","position":"Winger","position_cn":"边锋","club":"AEL Limassol","club_cn":"AEL利马索尔"},
    {"number":"25","name":"Chespan Moremi","name_cn":"切潘·莫雷米","position":"Forward","position_cn":"前锋","club":"Orlando Pirates","club_cn":"奥兰多海盗"},
    {"number":"26","name":"Mbekezeli Mbokazi","name_cn":"姆贝凯泽利·姆博卡齐","position":"Defender","position_cn":"后卫","club":"Chicago Fire","club_cn":"芝加哥火焰"},
]}

# ===== B组 =====
S["Canada"] = {"coach": "杰西·马什", "players": [
    {"number":"1","name":"Dayne St. Clair","name_cn":"戴恩·圣克莱尔","position":"Goalkeeper","position_cn":"门将","club":"Minnesota United","club_cn":"明尼苏达联"},
    {"number":"16","name":"Maxime Crépeau","name_cn":"马克西姆·克雷波","position":"Goalkeeper","position_cn":"门将","club":"Portland Timbers","club_cn":"波特兰伐木者"},
    {"number":"18","name":"Jonathan Sirois","name_cn":"乔纳森·西罗伊斯","position":"Goalkeeper","position_cn":"门将","club":"CF Montréal","club_cn":"蒙特利尔CF"},
    {"number":"2","name":"Alistair Johnston","name_cn":"阿利斯泰尔·约翰斯顿","position":"Right-Back","position_cn":"右后卫","club":"Celtic","club_cn":"凯尔特人"},
    {"number":"3","name":"Alphonso Davies","name_cn":"阿方索·戴维斯","position":"Left-Back","position_cn":"左后卫","club":"Bayern Munich","club_cn":"拜仁慕尼黑"},
    {"number":"4","name":"Derek Cornelius","name_cn":"德里克·科尼利厄斯","position":"Centre-Back","position_cn":"中后卫","club":"Marseille","club_cn":"马赛"},
    {"number":"5","name":"Moïse Bombito","name_cn":"莫伊兹·邦比托","position":"Centre-Back","position_cn":"中后卫","club":"Nice","club_cn":"尼斯"},
    {"number":"13","name":"Richie Laryea","name_cn":"里奇·拉里亚","position":"Defender","position_cn":"后卫","club":"Toronto FC","club_cn":"多伦多FC"},
    {"number":"15","name":"Kamal Miller","name_cn":"卡马尔·米勒","position":"Centre-Back","position_cn":"中后卫","club":"Portland Timbers","club_cn":"波特兰伐木者"},
    {"number":"22","name":"Joel Waterman","name_cn":"乔尔·沃特曼","position":"Defender","position_cn":"后卫","club":"CF Montréal","club_cn":"蒙特利尔CF"},
    {"number":"6","name":"Stephen Eustáquio","name_cn":"斯蒂芬·欧斯塔基奥","position":"Central Midfield","position_cn":"中前卫","club":"FC Porto","club_cn":"波尔图"},
    {"number":"7","name":"Tajon Buchanan","name_cn":"塔琼·布坎南","position":"Winger","position_cn":"边锋","club":"Inter Milan","club_cn":"国际米兰"},
    {"number":"8","name":"Ismaël Koné","name_cn":"伊斯梅尔·科内","position":"Central Midfield","position_cn":"中前卫","club":"Marseille","club_cn":"马赛"},
    {"number":"14","name":"Mathieu Choinière","name_cn":"马修·舒瓦尼埃","position":"Midfielder","position_cn":"中场","club":"CF Montréal","club_cn":"蒙特利尔CF"},
    {"number":"21","name":"Jonathan Osorio","name_cn":"乔纳森·奥索里奥","position":"Central Midfield","position_cn":"中前卫","club":"Toronto FC","club_cn":"多伦多FC"},
    {"number":"9","name":"Cyle Larin","name_cn":"赛尔·拉林","position":"Centre-Forward","position_cn":"中锋","club":"Mallorca","club_cn":"马略卡"},
    {"number":"10","name":"Jonathan David","name_cn":"乔纳森·戴维","position":"Centre-Forward","position_cn":"中锋","club":"Lille","club_cn":"里尔"},
    {"number":"11","name":"Liam Millar","name_cn":"利亚姆·米勒","position":"Winger","position_cn":"边锋","club":"FC Basel","club_cn":"巴塞尔"},
    {"number":"17","name":"Jacen Russell-Rowe","name_cn":"杰森·拉塞尔-罗","position":"Forward","position_cn":"前锋","club":"Columbus Crew","club_cn":"哥伦布机员"},
    {"number":"19","name":"Iké Ugbo","name_cn":"伊克·乌格博","position":"Centre-Forward","position_cn":"中锋","club":"Sheffield Wednesday","club_cn":"谢周三"},
    {"number":"20","name":"Theo Corbeanu","name_cn":"特奥·科尔贝亚努","position":"Winger","position_cn":"边锋","club":"Granada","club_cn":"格拉纳达"},
    {"number":"23","name":"Luca Koleosho","name_cn":"卢卡·科莱奥肖","position":"Forward","position_cn":"前锋","club":"Burnley","club_cn":"伯恩利"},
    {"number":"12","name":"Steven Vitória","name_cn":"史蒂文·维多利亚","position":"Centre-Back","position_cn":"中后卫","club":"Chaves","club_cn":"查韦斯"},
    {"number":"24","name":"Ali Ahmed","name_cn":"阿里·艾哈迈德","position":"Midfielder","position_cn":"中场","club":"Vancouver Whitecaps","club_cn":"温哥华白帽"},
    {"number":"25","name":"Kyle Hiebert","name_cn":"凯尔·希伯特","position":"Defender","position_cn":"后卫","club":"St. Louis City","club_cn":"圣路易斯城"},
    {"number":"26","name":"Ayo Akinola","name_cn":"阿约·阿基诺拉","position":"Forward","position_cn":"前锋","club":"San Jose Earthquakes","club_cn":"圣何塞地震"},
]}

# Add more teams in following groups...
# Due to space, let me add remaining teams in compact format
# ===== Build remaining teams from collected data =====

# I'll write the remaining teams more compactly
more_teams = {}

# C组: Morocco, Haiti, Scotland
more_teams["Morocco"] = {"coach":"Mohamed Ouahbi","players":[{"number":"1","name":"Yassine Bounou","name_cn":"亚辛·布努","position":"Goalkeeper","position_cn":"门将","club":"Al-Hilal","club_cn":"利雅得新月"},{"number":"12","name":"Munir El Kajoui","name_cn":"穆尼尔·卡维","position":"Goalkeeper","position_cn":"门将","club":"RS Berkane","club_cn":"RS贝尔卡内"},{"number":"22","name":"Ahmed Reda Tagnaouti","name_cn":"艾哈迈德·塔格纳乌蒂","position":"Goalkeeper","position_cn":"门将","club":"AS FAR","club_cn":"皇家武装部队"},{"number":"2","name":"Achraf Hakimi","name_cn":"阿什拉夫·哈基米","position":"Right-Back","position_cn":"右后卫","club":"Paris SG","club_cn":"巴黎圣日耳曼"},{"number":"3","name":"Noussair Mazraoui","name_cn":"努赛尔·马兹拉维","position":"Left-Back","position_cn":"左后卫","club":"Manchester United","club_cn":"曼联"},{"number":"5","name":"Nayef Aguerd","name_cn":"纳耶夫·阿格尔德","position":"Centre-Back","position_cn":"中后卫","club":"Marseille","club_cn":"马赛"},{"number":"6","name":"Chadi Riad","name_cn":"沙迪·里亚德","position":"Centre-Back","position_cn":"中后卫","club":"Crystal Palace","club_cn":"水晶宫"},{"number":"4","name":"Issa Diop","name_cn":"伊萨·迪奥普","position":"Centre-Back","position_cn":"中后卫","club":"Fulham","club_cn":"富勒姆"},{"number":"8","name":"Sofyan Amrabat","name_cn":"索菲扬·阿姆拉巴特","position":"Defensive Midfield","position_cn":"防守中场","club":"Real Betis","club_cn":"皇家贝蒂斯"},{"number":"10","name":"Azzedine Ounahi","name_cn":"阿泽丁·乌纳希","position":"Central Midfield","position_cn":"中前卫","club":"Girona","club_cn":"赫罗纳"},{"number":"15","name":"Bilal El Khannouss","name_cn":"比拉尔·汉努斯","position":"Attacking Midfield","position_cn":"攻击中场","club":"Stuttgart","club_cn":"斯图加特"},{"number":"14","name":"Ismael Saibari","name_cn":"伊斯梅尔·赛巴里","position":"Central Midfield","position_cn":"中前卫","club":"PSV Eindhoven","club_cn":"PSV埃因霍温"},{"number":"18","name":"Ayyoub Bouaddi","name_cn":"阿尤布·布阿迪","position":"Midfielder","position_cn":"中场","club":"Lille","club_cn":"里尔"},{"number":"7","name":"Brahim Díaz","name_cn":"卜拉欣·迪亚斯","position":"Attacking Midfield","position_cn":"攻击中场","club":"Real Madrid","club_cn":"皇家马德里"},{"number":"17","name":"Abde Ezzalzouli","name_cn":"阿卜德·埃扎尔祖利","position":"Left Wing","position_cn":"左边锋","club":"Real Betis","club_cn":"皇家贝蒂斯"},{"number":"9","name":"Ayoub El Kaabi","name_cn":"阿尤布·卡比","position":"Centre-Forward","position_cn":"中锋","club":"Olympiacos","club_cn":"奥林匹亚科斯"},{"number":"11","name":"Soufiane Rahimi","name_cn":"苏菲安·拉希米","position":"Forward","position_cn":"前锋","club":"Al Ain","club_cn":"艾因"},{"number":"19","name":"Chemsdine Talbi","name_cn":"切姆西丁·塔尔比","position":"Forward","position_cn":"前锋","club":"Sunderland","club_cn":"桑德兰"},{"number":"20","name":"Yassine Gessime","name_cn":"亚辛·格西姆","position":"Forward","position_cn":"前锋","club":"Strasbourg","club_cn":"斯特拉斯堡"},{"number":"21","name":"Ayoube Amaimouni","name_cn":"阿尤布·阿迈穆尼","position":"Forward","position_cn":"前锋","club":"Eintracht Frankfurt","club_cn":"法兰克福"},{"number":"13","name":"Zakaria El Ouahdi","name_cn":"扎卡里亚·瓦赫迪","position":"Defender","position_cn":"后卫","club":"Genk","club_cn":"亨克"},{"number":"16","name":"Neil El Aynaoui","name_cn":"尼尔·艾纳维","position":"Midfielder","position_cn":"中场","club":"Roma","club_cn":"罗马"},{"number":"23","name":"Redouane Halhal","name_cn":"雷杜万·哈尔哈尔","position":"Defender","position_cn":"后卫","club":"KV Mechelen","club_cn":"梅赫伦"},{"number":"24","name":"Youssef Belammari","name_cn":"优素福·贝拉马里","position":"Defender","position_cn":"后卫","club":"Al Ahly","club_cn":"开罗国民"},{"number":"25","name":"Anass Salah-Eddine","name_cn":"阿纳斯·萨拉赫丁","position":"Defender","position_cn":"后卫","club":"PSV Eindhoven","club_cn":"PSV埃因霍温"},{"number":"26","name":"Samir El Mourabet","name_cn":"萨米尔·穆拉贝","position":"Midfielder","position_cn":"中场","club":"Strasbourg","club_cn":"斯特拉斯堡"}]}

# Save incrementally
json.dump(S | more_teams, open('wiki_squads_partial.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"Part 1: {len(S) + len(more_teams)} teams written")
