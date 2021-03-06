from bs4 import BeautifulSoup
import requests
import time
import random
import re
import telebot
import config as conf

TOKEN_TG = conf.token
ID_USER_TELEGRAM = conf.id_user_telegram

USER_AGENT = conf.user_agent
URL = "https://www.avito.ru/krasnodar/tovary_dlya_kompyutera/komplektuyuschie/korpusy-ASgBAgICAkTGB~pm7gnEZw?s=104"


def send_an_ad():
    bot = telebot.TeleBot(TOKEN_TG)
    while True:
        bot.send_message(ID_USER_TELEGRAM, 'https://www.avito.ru' + check_new_ad())


def check_new_ad():
    old_pars_website = take_info()
    while True:
        time.sleep(random.randint(200, 350))
        new_pars_website = take_info()

        if not new_pars_website:
            continue

        for item in new_pars_website:
            if item not in old_pars_website:
                old_pars_website.add(item)
                return item


def take_info():
    ad_site = set()
    responce = requests.get(URL, headers={'user-agent': USER_AGENT})
    print(responce)
    soup = BeautifulSoup(responce.content, 'html.parser')
    items = soup.findAll('div',
                         class_='items-items-38oUm',
                         limit=6)
    informat = []

    for item in items:
        informat.append(str(
            item.find('a', class_='iva-item-sliderLink-2hFV_')
        ))
        for info in informat:
            re_website = re.findall(r'/krasnodar.+_[0-9]+', info)
            ad_site.add(str(*re_website))

    return ad_site


if __name__ == '__main__':
    send_an_ad()
