import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import math
import time
from def_math import create
import numpy as np

#id группы и токен, важны для авторизации, токен - это конфиденциальная информация, как пароль
group_id=187481546
token = "b54d45ce2605f72ee78b3d9b2abe5b874dd584f7d17e4374a4a520b86ccd90a269e07345336d920b7467f"



def main():
    dict_dialog_flag = {}
    #подкачивает словарь с данными
    dict_user = np.load("data.npy")
    admins = [184369782, 169374237, 58875285]
    dict_ping = []
    print("Started")
    #Авторизация в вк
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id)
    #словарь с уровнями
    lvls = {1: {'plus': [[1, 50], [1, 50]], 'multi': [[1, 10], [1, 10]], 'minus': [[1, 100], [1, 60]], 'div': [[1, 10], [1, 10]], 'sq': [[1, 10]], 'degree': [[1, 10], [2, 2]]},
            2: {'plus': [[100, 500], [100, 500]], 'multi': [[10, 32], [10, 32]], 'minus': [[500, 1000], [100, 600]], 'div': [[10, 32], [10, 32]], 'sq': [[5, 25]], 'degree': [[5, 7], [3, 3]]},
            3: {'plus': [[800, 5000], [800, 5000]], 'multi': [[20, 100], [20, 100]], 'minus': [[5000, 10000], [1000, 6000]], 'div': [[30, 100], [30, 100]], 'sq': [[30, 50]], 'degree': [[7, 10], [4, 4]]}}
    def primer_create(lvls, event, lvl):
        mass = lvls[lvl]
        if lvl == 3:
            choose_num = random.randint(1, 7)
        else:
            choose_num = random.randint(1, 6)
        if choose_num == 1:
            otvet = create.plus(mass)
        elif choose_num == 2:
            otvet = create.multi(mass)
        elif choose_num == 3:
            otvet = create.minus(mass)
        elif choose_num == 4:
            otvet = create.div(mass)
        elif choose_num == 5:
            otvet = create.sq(mass)
        elif choose_num == 6:
            otvet = create.degree(mass)
        elif choose_num == 7:
            otvet = create.equation(mass)
        primer_txt = otvet[0]
        primer_answer = otvet[1]
        # отправляет пример в диалог
        vk_session.method("messages.send",
                          {"peer_id": event.obj.peer_id, "message": primer_txt,
                           "random_id": random.randint(1, 2147483647)})
        return primer_answer



#"слушает" сервер вк, ждет получение какого либо события, один из которых Message_New
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:

            #point1 и point2 временные точки, по которым определяется скорость обработки
            point1 = time.perf_counter()
            #записывает нужные постоянные из словаря по ключам, если до этого не было создано никаких разделов, то выводит в стандарт
            try:
                answer_status = dict_dialog_flag[event.obj.peer_id]["answer_status"]
                primer_answer = dict_dialog_flag[event.obj.peer_id]["primer_answer"]
                lvl = dict_dialog_flag[event.obj.peer_id]["lvl"]
                last_question_time = dict_dialog_flag[event.obj.peer_id]["last_question_time"]
            except:
                print("New User")
                answer_status = True
                primer_answer = None
                lvl = 1
                last_question_time = None
                dict_dialog_flag.update([(event.obj.peer_id, {})])
            try:
                #вытаскивает из словаря нужные переменные, если таковых нету(пользователь не зарегистрирован), то ставит по нулям
                ranswer_time = dict_user[0][event.obj.from_id]["ranswer_time"]
                ranswers = dict_user[0][event.obj.from_id]["ranswers"]
                fanswers = dict_user[0][event.obj.from_id]["fanswers"]
            except:
                ranswer_time = [0,0,0]
                ranswers = [0,0,0]
                fanswers = [0,0,0]
                dict_user[0].update([(event.obj.from_id, {})])
            #dev - помощник для разработчика, позволяющий выполнять команды через интерфейс
            if event.obj.text.lower()[0:3] == "dev" and event.obj.from_id in admins:
                try:
                    vk_session.method("messages.send",
                                      {"peer_id": event.obj.peer_id,
                                       "message": str(eval(event.obj.text[4:len(event.obj.text)])),
                                       "random_id": random.randint(1, 2147483647)})
                except:
                    vk_session.method("messages.send",
                                     {"peer_id": event.obj.peer_id,
                                      "message": "None",
                                      "random_id": random.randint(1, 2147483647)})


            if "!начать" in event.obj.text.lower().split(" "):
                #определяет уровень сложности
                if len(event.obj.text.split(" ")) == 1:
                    lvl = 1
                else:
                    print(event.obj.text.split(" ")[1])
                    try:
                        lvl = int(event.obj.text.split(" ")[1])
                        if lvl>3:
                            lvl=1
                    except: lvl = 1

                #Создает пример
                primer_answer = primer_create(lvls, event, lvl)
                last_question_time = time.time()
                answer_status = False

            elif event.obj.text.lower() == "!конец" and answer_status == False:
                answer_status = True
                vk_session.method("messages.send",
                                  {"peer_id": event.obj.peer_id, "message": "Понял, выключаю",
                                   "random_id": random.randint(1, 2147483647)})
                last_question_time = None
            elif event.obj.text.lower() == "!инфо" or event.obj.text.lower() == "!информация" or event.obj.text.lower() == "!команды":
                vk_session.method("messages.send",
                                  {"peer_id": event.obj.peer_id,
                                   "message": "!начать (j) - начало работы (j = уровень сложности: 1, 2, 3) \n !конец - завершение работы \n !статистика - статистика ответов \n !очистить (j) - очистка статистики (j = выбор уровня: 1,2,3, все)",
                                   "random_id": random.randint(1, 2147483647)})

            elif event.obj.text.lower() == "!статистика":
                user_info = vk_session.method("users.get", {"user_ids": event.obj.from_id})
                try:
                    statistics1 = str(round(ranswer_time[0]/ranswers[0], 2)) + " сек"
                except:
                    statistics1 = "Отсутствует информация"
                try:
                    statistics2 = str(round(ranswer_time[1]/ranswers[1], 2)) + " сек"
                except:
                    statistics2 = "Отсутствует информация"
                try:
                    statistics3 = str(round(ranswer_time[2]/ranswers[2], 2)) + " сек"
                except:
                    statistics3 = "Отсутствует информация"

                statistics = "Статистика пользователя " + "[id"+str(event.obj.from_id)+"|" + user_info[0]["first_name"] + " " + user_info[0]["last_name"] + "]:" + "\n" + "--------------------------------" + "\n" + "Первый уровень:" + "\n" + "Среднее время ответа: " + statistics1  + "\n" + "Правильные ответы: " + str(ranswers[0])  + "\n" + "Ошибки: " + str(fanswers[0])  + "\n" + "--------------------------------" + "\n" + \
                             "Второй уровень: " + "\n" + "Среднее время ответа: " + statistics2  + "\n" + "Правильные ответы: " + str(ranswers[1])  + "\n" + "Ошибки: " + str(fanswers[1])  + "\n" + "--------------------------------" + "\n" + \
                             "Третий уровень: " + "\n" + "Среднее время ответа: " + statistics3  + "\n" + "Правильные ответы: " + str(ranswers[2])  + "\n" + "Ошибки: " + str(fanswers[2])  + "\n" + "--------------------------------" \


                vk_session.method("messages.send",
                                  {"peer_id": event.obj.peer_id,
                                   "message": statistics,
                                   "random_id": random.randint(1, 2147483647)})
            elif event.obj.text.lower().split(" ")[0] == "!очистить":
                if len(event.obj.text.lower().split(" "))>1:
                    if event.obj.text.lower().split(" ")[1] in ["1", "2", "3"]:
                        lvlnum = int(event.obj.text.lower().split(" ")[1])
                        ranswers[lvlnum - 1] = 0
                        ranswer_time[lvlnum - 1] = 0
                        fanswers[lvlnum - 1] = 0
                    elif event.obj.text.lower().split(" ")[1] in ["все", "всё", "all"]:
                        for i in range(3):
                            ranswers[i]=0
                            fanswers[i]=0
                            ranswer_time[i]=0
                    vk_session.method("messages.send",
                                      {"peer_id": event.obj.peer_id,
                                       "message": "Статистика очищена",
                                       "random_id": random.randint(1, 2147483647)})
                else:
                    vk_session.method("messages.send",
                                      {"peer_id": event.obj.peer_id,
                                       "message": "Некорректное значение",
                                       "random_id": random.randint(1, 2147483647)})


            #Проверяет ответ,если ответ верный, то создает новый пример
            if answer_status == False:
                if event.obj.text == str(primer_answer):
                    delta= time.time() - last_question_time
                    user_info = vk_session.method("users.get", {"user_ids": event.obj.from_id})
                    vk_session.method("messages.send",
                                      {"peer_id": event.obj.peer_id, "message": "[id"+str(event.obj.from_id)+"|" + user_info[0]["first_name"] + " " + user_info[0]["last_name"] + "] Правильный ответ! (" + str(round(delta, 1)) + " сек.)",
                                       "random_id": random.randint(1, 2147483647)})
                    ranswer_time[lvl-1] += delta
                    ranswers[lvl-1] += 1
                    primer_answer = primer_create(lvls,event,lvl)
                    last_question_time = time.time()

                else:
                        try:
                            if int(event.obj.text) != primer_answer:
                                vk_session.method("messages.send",
                                                  {"peer_id": event.obj.peer_id, "message": "Ответ неверный",
                                                   "random_id": random.randint(1, 2147483647)})
                                fanswers[lvl-1] += 1

                        except:
                            None
            #записывает нужные переменные в словарь
            dict_dialog_flag[event.obj.peer_id].update(answer_status=answer_status, primer_answer=primer_answer, lvl=lvl, last_question_time=last_question_time)

            #сохраняет данные в словарь
            dict_user[0][event.obj.from_id].update(ranswer_time=ranswer_time,ranswers=ranswers, fanswers=fanswers)
            np.save("data", dict_user)

            point2 = time.perf_counter()
            ping = point2-point1
            print("Время прошло:" + str(ping))
            dict_ping.append(ping)


















            #Вспомогательный вывод сообщений, типов событий в консоль
            print('Новое сообщение:')

            print('Для меня от: ', end='')

            print(event.obj.from_id)

            print('Текст:', event.obj.text)
            print()

        else:
            print(event.type)
            print()







if __name__ == '__main__':
    main()






