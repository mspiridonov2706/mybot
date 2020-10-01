import settings

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from random import randint, choice

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
      message = f'Ваше числов {user_number}, моё {bot_number}, вы выиграли'
    elif user_number == bot_number:
      message = f'Ваше числов {user_number}, моё {bot_number}, ничья'
    else:
      message = f'Ваше числов {user_number}, моё {bot_number}, вы проиграли'
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
      smile = choice(settings.USER_EMOJI)
      return emojize(smile, use_aliases=True)
    return user_data['emoji']

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Получить мемасик', KeyboardButton(text='Мои координаты', request_location=True)]
    ])