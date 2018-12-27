#  -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
import random
import requests
app = Flask(__name__)

def pick_lotto():
    numbers = random.sample(range(1, 46), 6)
    return numbers
    
def get_lotto(rounds):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}'.format(rounds)
    response = requests.get(url)
    lotto_data = response.json()
    numbers = []
    for key, value in lotto_data.items():
        if 'drwtNo' in key:
            numbers.append(value)
    numbers.sort()
    bonus_number = lotto_data['bnusNo']
    final_dict = { 
        "numbers": numbers,
         'bonus': bonus_number
         }
    return final_dict
    
def am_i_lucky(pick_num, draw_no):
    real_num = get_lotto(draw_no)
    match_number = len(set(pick_num) & set(real_num['numbers']))
    if match_number == 6:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '1등')
    elif match_number == 5 and real_num['bonus'] in pick_num:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '2등')
    elif match_number == 5:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '3등')
    elif match_number == 4:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '4등')
    elif match_number == 3:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '5등')
    else:
        return(pick_num, draw_no, real_num['numbers'], real_num['bonus'], match_number, '꼴등')

@app.route("/")
def index():
    numbers = sorted(random.sample(range(1, 46), 6))
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=837'
    lotto_data = requests.get(url).json()
    real_numbers = []
    for key in lotto_data:
        if 'drwtNo' in key:
            real_numbers.append(lotto_data[key])
    bonus_number = lotto_data['bnusNo']
    return render_template('index.html', numbers=numbers, real=real_numbers, bonus=bonus_number)

@app.route("/ping")
def ping():
    return render_template('ping.html')

@app.route("/pong")
def pong():
    ssum = request.args.get('ssum')
    me = request.args.get('me')
    result = me + '=>' + ssum
    match_point = random.choice(range(1, 100))
    
    MY_CHAT_ID = '751345255'
    BOT_TOKEN = '714587754:AAFFrK6l_ShZurmHQAO2doSGjB15Om5x3CI'
    
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, MY_CHAT_ID, result)

    response = requests.get(url)
    
    return render_template('pong.html', match_point=match_point, me=me, ssum=ssum)
    

@app.route('/amilucky')
def amilucky():
    rounds = request.args.get('rounds')
    my_numbers = pick_lotto()
    WYL = am_i_lucky(my_numbers, int(rounds))
    MY_CHAT_ID = '751345255'
    BOT_TOKEN = '714587754:AAFFrK6l_ShZurmHQAO2doSGjB15Om5x3CI'
    result = ("추첨 번호는", WYL[0], "입니다.", WYL[1], "회차 당첨 번호는", WYL[2], "입니다. 맞춘 갯수는", WYL[4], "개 입니다. 당신은", WYL[5], "입니다.")
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, MY_CHAT_ID, result)

    response = requests.get(url)
    
    return render_template('amilucky.html', pick_num=WYL[0], real_num=WYL[2], bonus_num=WYL[3], match_num=WYL[4], result=WYL[5], rounds=rounds)

@app.route('/raccooncho')
def raccoon():
    return render_template('introduction.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
