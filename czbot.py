import vk_api
import random
import time
import json
import pymysql.cursors
import re

token = "58dc9b12fc8ee2f5445a8507e3258a7a10f03c66cb2d07d54d8f65f7b38592af77c91802dacdc259cd07f"

connect = pymysql.connect(host='85.10.205.173',
                             user='czbot_database',
                             password='czbot_database',
                             db='czbot_database',
                             charset='utf8mb4'
                             )

vk = vk_api.VkApi(token=token)
vk._auth_token()

file = open("data.txt" , "r")
data = json.load(file)

dz = data[0]
print(dz)
file.close()

def save():
    saves = []
    saves.append(dz)
    file = open("data.txt" , "w")
    json.dump(saves, file)
    file.close()


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }
keyboard = {"buttons":[[get_button(label="Информация", color="default"),get_button(label="Сеанс", color="default")],[get_button(label="Подписаться", color="positive")]],"one_time": False}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            user_info = vk.method("users.get", {"user_ids": id, "name_case": "Nom"})
            full_name = user_info[0]["first_name"]+" "+user_info[0]["last_name"]
            if body.lower() == "информация":
                vk.method("messages.send", {"peer_id": id,"keyboard": keyboard, "message": "Привет! Это бот корпорации Crime Zoo LLC. Я могу проинформировать тебя о ближайших сеансах czCinema.", "random_id": random.randint(1, 2147483647)})
            elif body.lower() == "сеанс":
                vk.method("messages.send", {"peer_id": id,"keyboard": keyboard, "attachment":"photo427008202_457239140", "message": str(dz), "random_id": random.randint(1, 2147483647)})
            elif body.lower() == "подписаться":
            	with connect.cursor() as cursor:
            		cursor.execute("select count(*) from `subscribers` where `username` = '"+full_name+"'")
            		count_accounts = cursor.fetchall()
            		result = re.findall(r"\d*",str(count_accounts))
            		if int(result[2]) == 0:
            			cursor.execute("insert into `subscribers`(`username`, `token`) values ('"+full_name+"', '"+str(id)+"')")
            			vk.method("messages.send", {"peer_id": id,"keyboard": keyboard, "message": "✅  Ура! Подписка оформлена, теперь ты будешь в курсе, если в czCinema начнётся сеанс! ", "random_id": random.randint(1, 2147483647)})
            			print("добавили")
            			print(result[2])
	            	else:
	            		print("существует")
	            		print(result[2])
	            		vk.method("messages.send", {"peer_id": id,"keyboard": keyboard, "message": "Вы уже подписаны на рассылку! ", "random_id": random.randint(1, 2147483647)})

            		connect.commit()
            		#if int(count_accounts) > 0:
	            	#	cursor.execute("insert into `subscribers`(`username`, `token`) values ('"+full_name+"', '"+str(id)+"')")
	            	#	print("добавили")
	            	#else:
	            	#	print("существует")
            elif body.lower() == "отписаться":
                vk.method("messages.send", {"peer_id": id,"keyboard": keyboard, "message": "😢😭😟 Подписка на оповещения о начале стрима отключена :(\nЕсли передумаешь, нажми кнопку \"Подписаться\", я всё прощу.", "random_id": random.randint(1, 2147483647)})
            else:
                a = list(body)
                b = 6
                data = ""
                while b>=0:
                    b = b - 1
                    data = str(data) + str(a[0])
                    a.pop(0)
                if data == "/update":
                    b = len(a)
                    zap = ""
                    if b >=1:
                        for i in a:
                            zap = str(zap) + str(i)
                        dz = zap
                        vk.method("messages.send", {"peer_id": id, "message": "✅ Информация о сеансе обновлена.", "random_id": random.randint(1, 2147483647)})
                        vk.method("messages.send", {"peer_id": id, "message": "\"" + dz + "\"", "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send", {"peer_id": id, "message": "На данный момент нет запланированных сеансов.", "random_id": random.randint(1, 2147483647)})

                save()
    except Exception as E:
        time.sleep(1)


