"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""

import datetime
import ephem
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    logging.info('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')
    logging.info("Бот ответил")

def planet(update, context):
    logging.info('Вызван /planet')
    now = datetime.datetime.now()
    mars = ephem.Mars(now)
    planet_name = f'Планета: {mars.name}'
    stars = ephem.constellation(mars)
    star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета {mars.name} находится в созвездии {stars[1]}'
    update.message.reply_text(star_planet)
    logging.info(star_planet)

def planet_constellation(update, context):
    user_text = update.message.text 
    logging.info(user_text)
    if user_text.lower() == 'mars':
        now = datetime.datetime.now()
        mars = ephem.Mars(now)
        planet_name = f'Планета: {mars.name}'
        stars = ephem.constellation(mars)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета {mars.name} находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet)
    else:
        update.message.reply_text(f'Такой планеты нет в моей базе')
    logging.info(star_planet)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(MessageHandler(Filters.text, planet_constellation))
    
    logging.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
