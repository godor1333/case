# from datetime import datetime
# from flask import render_template, flash, redirect, url_for, request, g, \
#     jsonify, current_app
# from app.main import bp




# @bp.route('/', methods=['GET', 'POST'])
# def r():
#     return '<h1>123</h1>'

from app.api import bp
from database.database import question_db, notifications_db
from flask import request
from flask import Response
import json
from flask import Response
# from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
import requests
from flask import request
from app.main import bp

token = '964366098:AAHVQmvayZIXEDHyIZOY1dDo0_t8oFOVnCY'
#ner = build_model(configs.ner.ner_rus_bert, download=False)
#Чтобы обучить на новых данных измените train=True
# faq = SimilarityMatchingSkill(
#   data_path ='faq_school.csv',
#   x_col_name = 'Question',
#   y_col_name = 'Answer',
#   #config_path = str(os.getcwd()) + '/config.json',
#   edit_dict = {},
#   train = False
# )

#server.config.from_object(config.Config)



@bp.route('/', methods=['POST', 'GET'])
def bot():
    if request.method == 'POST':
        msg = request.get_json()
        print('asdgs')
        chat_id, text = parse_msg(msg)

        # text, chat_id -> текст пользователя, который написал боту и id чата

        # if '/' in text:
        #     send_msg(chat_id, 'Wrong command')
        #     return Response('ok', status=200)

        send_msg(chat_id, text)
        return Response('ok', status=200)
    else:
        return '<h1>tg-bot-1crs</h1>'


def parse_msg(message):
    print('paees')
    id = message['message']['chat']['id']
    text = message['message']['text']

    return id, text


def send_msg(chat_id, text='123'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    # answer = faq([text],[],[])
    s= ""
    # sett = {'chat_id': chat_id, 'text':''.join(answer[0])}
    sett = {'chat_id': chat_id, 'text': 'loh'}
    r = requests.post(url, json=sett)
    return r
  


@bp.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        data = request.get_json()
        question_db.add_answer(data['question'], data['defaultAnswer'], data['type'])
        return Response('ok', status=200)
    else:
        return json.dumps(question_db.get_questions_and_answers())

@bp.route('/delete/question/<id>', methods=['DELETE'])
def del_question(id):
    if request.method == 'DELETE':
        question_db.delete_answer("q" + id)
        return Response('ok', status=200)

@bp.route('/change/question', methods=['POST'])
def ch_question():
    if request.method == 'POST':
        data = request.get_json()
        if 'group' in data:
            question_db.change_answer("q" + data['id'], data['text'], data['group'], data['author'])
        else:
            question_db.change_answer("q" + data['id'], data['text'])
        return Response('ok', status=200)

@bp.route('/notifications', methods=['GET', 'POST', 'DELETE'])
def notifications():
    if request.method == 'POST':
        data = request.get_json()
        notifications_db.add_notification(data['text'], data['data'], data['group'])
        return Response('ok', status=200)
    else:
        return json.dumps(notifications_db.get_notifications())

@bp.route('/delete/notifications/<data>', methods=['DELETE'])
def del_notifications(data):
    if request.method == 'DELETE':
        notifications_db.delete_notifications_by_data(data)
        return Response('ok', status=200)
token = '964366098:AAHVQmvayZIXEDHyIZOY1dDo0_t8oFOVnCY'

Tbot = telebot.TeleBot('964366098:AAHVQmvayZIXEDHyIZOY1dDo0_t8oFOVnCY')
print("asdf")


#ner = build_model(configs.ner.ner_rus_bert, download=False)
#Чтобы обучить на новых данных измените train=True
faq = SimilarityMatchingSkill(
  data_path ='faq.csv',
  x_col_name = 'Question',
  y_col_name = 'Answer',
  #config_path = str(os.getcwd()) + '/config.json',
  edit_dict = {},
  train = question_db.is_network_update()
)
#print("asdf")
#bot.polling(none_stop=True)
#server.config.from_object(config.Config)
#print("asdf")

#@bp.route('/bot', methods=['POST', 'GET'])
@Tbot.message_handler(content_types=['text'])
def handle_text(message):
    print("answer")
    #if request.method == 'POST':
       # msg = request.get_json()
        #print('asdgs')
    #chat_id, text = parse_msg(message)


    
    # not_list = notifications_db.get_notifications()
    # for a in not_list:
    #     print('ewrfcd')
    #     C_T(a['data'],a['text'],a['group'])
    #     time.sleep(60)


    if str(message.from_user.id) in students_db.get_all_students():
        id_ = faq([message.text], [], [])[0][0]
        if faq([message.text], [], [])[1][0] < 0.25:
            print( faq([message.text], [], [])[1][0])
            answer = "Невозможно верно распознать вопрос"    
        else:
            answer = question_db.get_answer(id_,students_db.get_student_by_tgid(message.from_user.id))
        Tbot.send_message(message.from_user.id, answer)
    else:
        if len(message.text) == 4 and message.text.isdigit():
            students_db.add_student(message.from_user.id,message.text)
            return 
        Tbot.send_message(message.from_user.id, answer)

    #send_msg(chat_id, text)
    # text, chat_id -> текст пользователя, который написал боту и id чата

        # if '/' in text:
        #     send_msg(chat_id, 'Wrong command')
        #     return Response('ok', status=200)


    #     return Response('ok', status=200)
    # else:
    #     return '<h1>tg-bot-1crs</h1>'


def parse_msg(message):
    #print('paees')
    id = message['message']['chat']['id']
    text = message['message']['text']

    return id, text
