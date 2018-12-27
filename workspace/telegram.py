import requests
import random

MY_CHAT_ID = '751345255'
BOT_TOKEN = '714587754:AAFFrK6l_ShZurmHQAO2doSGjB15Om5x3CI'
msg = 'helloraccooncho'

url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, MY_CHAT_ID, msg)

response = requests.get(url)
print(response.json())
