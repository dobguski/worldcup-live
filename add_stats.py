import json
details = json.load(open('player_details.json', encoding='utf-8'))

stats = {
    'Lionel Messi': {'club_goals':31,'club_apps':42,'intl_goals':112,'intl_apps':191,'career_goals':850,'career_apps':1087,'birth_date':'1987-06-24','birth_place':'Rosario, Argentina','nationality':'Argentina','age':38,'height':'170 cm','weight':'67 kg'},
    'Cristiano Ronaldo': {'club_goals':82,'club_apps':95,'intl_goals':135,'intl_apps':217,'career_goals':925,'career_apps':1240,'birth_date':'1985-02-05','birth_place':'Funchal, Portugal','nationality':'Portugal','age':41,'height':'187 cm','weight':'83 kg'},
    'Kylian Mbappe': {'club_goals':38,'club_apps':52,'intl_goals':48,'intl_apps':84,'career_goals':310,'career_apps':420,'birth_date':'1998-12-20','birth_place':'Paris, France','nationality':'France','age':27,'height':'178 cm','weight':'73 kg'},
    'Erling Haaland': {'club_goals':35,'club_apps':45,'intl_goals':38,'intl_apps':42,'career_goals':260,'career_apps':310,'birth_date':'2000-07-21','birth_place':'Leeds, England','nationality':'Norway','age':25,'height':'194 cm','weight':'88 kg'},
    'Harry Kane': {'club_goals':44,'club_apps':48,'intl_goals':69,'intl_apps':103,'career_goals':370,'career_apps':580,'birth_date':'1993-07-28','birth_place':'London, England','nationality':'England','age':32,'height':'188 cm','weight':'86 kg'},
    'Kevin De Bruyne': {'club_goals':12,'club_apps':38,'intl_goals':28,'intl_apps':105,'career_goals':150,'career_apps':600,'birth_date':'1991-06-28','birth_place':'Drongen, Belgium','nationality':'Belgium','age':35,'height':'181 cm','weight':'70 kg'},
    'Mohamed Salah': {'club_goals':28,'club_apps':42,'intl_goals':59,'intl_apps':105,'career_goals':310,'career_apps':600,'birth_date':'1992-06-15','birth_place':'Nagrig, Egypt','nationality':'Egypt','age':34,'height':'175 cm','weight':'71 kg'},
    'Neymar': {'club_goals':8,'club_apps':15,'intl_goals':79,'intl_apps':128,'career_goals':440,'career_apps':700,'birth_date':'1992-02-05','birth_place':'Mogi das Cruzes, Brazil','nationality':'Brazil','age':34,'height':'175 cm','weight':'68 kg'},
    'Lamine Yamal': {'club_goals':18,'club_apps':48,'intl_goals':4,'intl_apps':18,'career_goals':22,'career_apps':66,'birth_date':'2007-07-13','birth_place':'Esplugues de Llobregat, Spain','nationality':'Spain','age':18,'height':'178 cm','weight':'65 kg'},
    'Jude Bellingham': {'club_goals':18,'club_apps':40,'intl_goals':6,'intl_apps':40,'career_goals':60,'career_apps':220,'birth_date':'2003-06-29','birth_place':'Stourbridge, England','nationality':'England','age':22,'height':'186 cm','weight':'75 kg'},
    'Jamal Musiala': {'club_goals':15,'club_apps':38,'intl_goals':5,'intl_apps':38,'career_goals':55,'career_apps':180,'birth_date':'2003-02-26','birth_place':'Stuttgart, Germany','nationality':'Germany','age':23,'height':'184 cm','weight':'72 kg'},
    'Bukayo Saka': {'club_goals':16,'club_apps':42,'intl_goals':12,'intl_apps':43,'career_goals':70,'career_apps':250,'birth_date':'2001-09-05','birth_place':'London, England','nationality':'England','age':24,'height':'178 cm','weight':'65 kg'},
    'Pedri': {'club_goals':12,'club_apps':44,'intl_goals':2,'intl_apps':24,'career_goals':30,'career_apps':180,'birth_date':'2002-11-25','birth_place':'Tegueste, Spain','nationality':'Spain','age':23,'height':'174 cm','weight':'60 kg'},
    'Son Heung-min': {'club_goals':22,'club_apps':40,'intl_goals':51,'intl_apps':131,'career_goals':220,'career_apps':550,'birth_date':'1992-07-08','birth_place':'Chuncheon, South Korea','nationality':'South Korea','age':33,'height':'183 cm','weight':'78 kg'},
    'Takefusa Kubo': {'club_goals':14,'club_apps':40,'intl_goals':5,'intl_apps':35,'career_goals':40,'career_apps':200,'birth_date':'2001-06-04','birth_place':'Kawasaki, Japan','nationality':'Japan','age':25,'height':'173 cm','weight':'67 kg'},
    'Darwin Nunez': {'club_goals':22,'club_apps':42,'intl_goals':14,'intl_apps':32,'career_goals':120,'career_apps':280,'birth_date':'1999-06-24','birth_place':'Artigas, Uruguay','nationality':'Uruguay','age':26,'height':'187 cm','weight':'81 kg'},
}
for name, s in stats.items():
    if name in details:
        details[name].update(s)

json.dump(details, open('player_details.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
with_age = sum(1 for p in details.values() if p.get('age'))
with_stats = sum(1 for p in details.values() if p.get('club_goals'))
print(f'{len(details)} players, {with_age} with age, {with_stats} with club stats')
