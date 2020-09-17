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

def greet_user(update,context):
  logging.info('Вызван /start')
  update.message.reply_text(
    'Привет, пользователь! Ты вызвал команду /start.\n'
    '/planet <название_планеты> - узнать в каком созвездии находится планета;\n'
    '\tДоступные планеты: Марс, Венера, Юпитер.\n'
    '/next_full_monn - узнать когда ближайшее полнолуние;'
  )

def planet(update, context):
    print(context.args)
    logging.info(context.args)
    if context.args[0].lower() == 'марс':
        logging.info('вызвана команда /planet Марс')
        now = datetime.datetime.now()
        mars = ephem.Mars(now)
        stars = ephem.constellation(mars)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета Марс находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet)
    elif context.args[0].lower() == 'юпитер':
        logging.info('вызвана команда /planet Юпитер')
        now = datetime.datetime.now()
        jupiter = ephem.Jupiter(now)
        stars = ephem.constellation(jupiter)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета Юпитер находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet)
    elif context.args[0].lower() == 'венера':
        logging.info('вызвана команда /planet Венера')
        now = datetime.datetime.now()
        venus = ephem.Venus(now)
        stars = ephem.constellation(venus)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета Венера находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet)      
    else:
        logging.info('вызвана команда неизвестная планета')
        update.message.reply_text('Такой планеты нет в моём списке!')

def next_full_moon(update,context):
    logging.info('вызвана команда /next_full_moon')
    now = datetime.datetime.now()
    full_moon = ephem.next_full_moon(now)
    update.message.reply_text(f'Ближайшее полнолуние произойдёт: {full_moon}')   

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
