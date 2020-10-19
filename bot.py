import logging
import settings
from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, anketa_dontknow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import (greet_user, guess_number, send_python_meme, user_coordinates, planet, next_full_moon,
                      check_user_photo)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            'name': [MessageHandler(Filters.text, anketa_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            'comment': [CommandHandler('skip', anketa_skip), MessageHandler(Filters.text, anketa_comment)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                           anketa_dontknow)
        ]
    )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("meme", send_python_meme))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.regex('^(Получить мемасик)$'), send_python_meme))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
