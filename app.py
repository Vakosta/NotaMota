import telebot
from telebot import types

import config

fl = 0
i = 0
last_i = -1

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup.add('Нравится')
markup.add('Не смотрел')
markup.add('Не нравится')

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['game'])
def start(message):
    global fl
    bot.send_message(message.chat.id, config.MOVIES[0], reply_markup=markup)
    fl = 1


@bot.message_handler(content_types=['text'])
def echo(message):
    global fl, i
    if fl == 1:
        if message.text == 'Нравится':
            bot.send_message(message.chat.id, 1)
        elif message.text == 'Не нравится':
            bot.send_message(message.chat.id, 3)
        elif message.text == 'Не смотрел':
            bot.send_message(message.chat.id, 2)
        i += 1
        bot.send_message(message.chat.id, config.MOVIES[i], reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
