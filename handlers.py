import datetime
import ephem
import logging

from glob import glob
from random import randint, choice
from utils import play_random_numbers, main_keyboard, get_smile

def greet_user(update,context):
    logging.info('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      '/planet <название_планеты> - узнать в каком созвездии находится планета;\n'
      '\tДоступные планеты: Марс, Венера, Юпитер.\n'
      '/next_full_moon - узнать когда ближайшее полнолуние;\n'
      '/guess <число> - поиграть с ботом в числа;\n'
      f'/meme - увидеть мемасик по Python {context.user_data["emoji"]};',
      reply_markup=main_keyboard()
    )

def guess_number(update, context):
    logging.info('Вызван /guess')
    if context.args:
      try:
        user_number = int(context.args[0])
        message = play_random_numbers(user_number)
      except (TypeError, ValueError):
        message = 'Введите целое число'
    else:
      message = 'Введите число'
    update.message.reply_text(message, reply_markup=main_keyboard())
    
def send_python_meme(update, context):
    logging.info('Запрошен мемасик')
    python_meme = glob('images/python*.jp*g')
    random_meme = choice(python_meme)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(random_meme, 'rb'), reply_markup=main_keyboard())

def user_coordinates(update, context):
    logging.info("Запрошены координаты")
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
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
        update.message.reply_text(star_planet, reply_markup=main_keyboard())
    elif context.args[0].lower() == 'юпитер':
        logging.info('вызвана команда /planet Юпитер')
        now = datetime.datetime.now()
        jupiter = ephem.Jupiter(now)
        stars = ephem.constellation(jupiter)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета Юпитер находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet, reply_markup=main_keyboard())
    elif context.args[0].lower() == 'венера':
        logging.info('вызвана команда /planet Венера')
        now = datetime.datetime.now()
        venus = ephem.Venus(now)
        stars = ephem.constellation(venus)
        star_planet = f'Сегодняшняя дата {now.strftime("%d-%m-%Y %H:%M")}.\nПланета Венера находится в созвездии {stars[1]}'
        update.message.reply_text(star_planet, reply_markup=main_keyboard())      
    else:
        logging.info('вызвана команда неизвестная планета')
        update.message.reply_text('Такой планеты нет в моём списке!', reply_markup=main_keyboard())

def next_full_moon(update,context):
    logging.info('вызвана команда /next_full_moon')
    now = datetime.datetime.now()
    full_moon = ephem.next_full_moon(now)
    update.message.reply_text(f'Ближайшее полнолуние произойдёт: {full_moon}', reply_markup=main_keyboard())   
