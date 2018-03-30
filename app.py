import telebot
from telebot import types

import config
from model import *

current_chat = None

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup.add('Нравится')
markup.add('Не смотрел')
markup.add('Не нравится')

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    global current_chat
    current_chat = Chat.create(id=message.chat.id, rating_stage=True)

    bot.send_message(message.chat.id, config.MOVIES[0], reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo(message):
    global current_chat
    current_chat = Chat.get(Chat.id == message.chat.id)
    if current_chat.rating_stage:
        if message.text == 'Нравится':
            Action.create(chat_id=message.chat.id,
                          film=config.MOVIES[current_chat.step],
                          rating=True)
        elif message.text == 'Не нравится':
            Action.create(chat_id=message.chat.id,
                          film=config.MOVIES[current_chat.step],
                          rating=None)
        elif message.text == 'Не смотрел':
            Action.create(chat_id=message.chat.id,
                          film=config.MOVIES[current_chat.step],
                          rating=False)

        current_chat.step += 1
        bot.send_message(message.chat.id, config.MOVIES[current_chat.step], reply_markup=markup)
        current_chat.save()


if __name__ == '__main__':
    # init_db()  # При первом запуске раскомментировать
    bot.polling(none_stop=True)
