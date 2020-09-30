import datetime
import ephem
import logging
import settings
from emoji import emojize
from glob import glob
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
    logging.info('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      '/planet <название_планеты> - узнать в каком созвездии находится планета;\n'
      '\tДоступные планеты: Марс, Венера, Юпитер.\n'
      '/next_full_moon - узнать когда ближайшее полнолуние;\n'
      '/guess <число> - поиграть с ботом в числа;\n'
      f'/meme - увидеть мемасик по Python {context.user_data["emoji"]};'
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

def guess_number(update, context):
    if context.args:
      try:
        user_number = int(context.args[0])
        message = play_random_numbers(user_number)
      except (TypeError, ValueError):
        message = 'Введите целое число'

    else:
      message = 'Введите число'
    update.message.reply_text(message)

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
      message = f'Ваше числов {user_number}, моё {bot_number}, вы выиграли'
    elif user_number == bot_number:
      message = f'Ваше числов {user_number}, моё {bot_number}, ничья'
    else:
      message = f'Ваше числов {user_number}, моё {bot_number}, вы проиграли'
    return message

def send_python_meme(update, context):
    python_meme = glob('images/python*.jp*g')
    random_meme = choice(python_meme)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(random_meme, 'rb'))

def get_smile(user_data):
    if 'emoji' not in user_data:
      smile = choice(settings.USER_EMOJI)
      return emojize(smile, use_aliases=True)
    return user_data['emoji']

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("meme", send_python_meme))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
