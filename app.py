import telebot

import config
import db

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    db.init()

    bot.polling(none_stop=True)
