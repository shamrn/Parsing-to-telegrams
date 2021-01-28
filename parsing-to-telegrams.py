from bs4 import BeautifulSoup
import requests
import time
import random
import re
import telebot
import config as c

TOKEN_TG = c.token
USER_AGENT = c.user_agent
ID_USER_TELEGRAM = c.id_user_telegram

bot = telebot.TeleBot(TOKEN_TG)

URL = "https://www.avito.ru/krasnodar/tovary_dlya_kompyutera/komplektuyuschie/korpusy-ASgBAgICAkTGB~pm7gnEZw?s=104"

def take_info(website):
    responce = requests.get(URL, headers=USER_AGENT)
    soup = BeautifulSoup(responce.content, 'html.parser')
    items = soup.findAll('div',
                         class_='iva-item-root-G3n7v photo-slider-slider-15LoY iva-item-list-2_PpT items-item-1Hoqq items-listItem-11orH js-catalog-item-enum',
                         limit=4)
    informat = []

    for item in items:
        informat.append(str(
            item.find('a', class_='iva-item-sliderLink-2hFV_')
        ))
        for info in informat:
            re_website = re.findall(r'/krasnodar.+_[0-9]+', info)
            website.add(str(*re_website))


old_pars_website = set()
take_info(old_pars_website)
if not old_pars_website:
    take_info(old_pars_website)

while True:
    time.sleep(random.randint(200, 350))

    new_pars_website = set()
    take_info(new_pars_website)
    if not new_pars_website:
        continue

    for item in new_pars_website:
        if item not in old_pars_website:
            bot.send_message(ID_USER_TELEGRAM, 'https://www.avito.ru' + item)
            old_pars_website.add(item)
