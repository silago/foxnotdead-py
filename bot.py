from telegram.ext import Updater, CommandHandler

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater('590889402:AAG-OPeK9bJAPdNU_9h_WXYs7e8eLfZBy7E')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
