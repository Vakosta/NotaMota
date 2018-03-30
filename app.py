import telebot

import config
import markups
import utils
from model import *

current_chat = None

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

film_of_one_film_rate = None
min_dist_film = ''


def send_film(id):
    film = MOVIES[current_chat.step]
    bot.send_message(id, film, reply_markup=markups.markup_like_or_not_or_not_watched)
    current_chat.current_film = config.MOVIES[current_chat.step]


@bot.message_handler(commands=['start'])
def start(message):
    global current_chat

    current_chat = Chat.get_or_create(id=message.chat.id)[0]

    bot.send_message(message.chat.id, config.MOVIES[0], reply_markup=markups.markup_like_or_not_or_not_watched)
    current_chat.current_film = config.MOVIES[0]
    current_chat.save()


@bot.message_handler(commands=['rate'])
def one_film_rate(message):
    global current_chat

    try:
        current_chat = Chat.get(Chat.id == message.chat.id)
    except Exception:
        start(message)
        return

    current_chat.one_film_rate = 1
    current_chat.save()

    bot.send_message(message.chat.id, 'Введите название фильма:')


@bot.message_handler(content_types=['text'])
def echo(message):
    global current_chat, film_of_one_film_rate, min_dist_film

    try:
        current_chat = Chat.get(Chat.id == message.chat.id)
    except Exception:
        start(message)
        return

    if current_chat.one_film_rate == 0:
        if message.text == 'Нравится':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=3)
        elif message.text == 'Нейтрально':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=2)
        elif message.text == 'Не нравится':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=1)
        elif message.text == 'Не смотрел':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=0)
        current_chat.step += 1
        bot.send_message(message.chat.id, 'Голос засчитан')
        send_film(message.chat.id)
    elif current_chat.one_film_rate == 1:
        min_dist = 100000000
        for i in config.MOVIES:
            dist = utils.distance(i.lower(), message.text.lower())
            if dist == 0:
                film_of_one_film_rate = i
                current_chat.one_film_rate = 2
                bot.send_message(message.chat.id, 'Оцените фильм.',
                                 reply_markup=markups.markup_like_or_not)
                current_chat.save()
                return
            else:
                if dist < min_dist:
                    min_dist = dist
                    min_dist_film = i
        bot.send_message(message.chat.id, 'Возможно вы имели ввиду ' + min_dist_film + '?',
                         reply_markup=markups.markup_yes_or_no)
        current_chat.one_film_rate = 3
    elif current_chat.one_film_rate == 2:
        if message.text == 'Нравится':
            Action.create(chat_id=message.chat.id,
                          film=film_of_one_film_rate,
                          rating=True)
        elif message.text == 'Не нравится':
            Action.create(chat_id=message.chat.id,
                          film=film_of_one_film_rate,
                          rating=None)
        elif message.text == 'Не смотрел':
            Action.create(chat_id=message.chat.id,
                          film=film_of_one_film_rate,
                          rating=False)
        current_chat.one_film_rate = 0
        bot.send_message(message.chat.id, 'Голос засчитан')
        send_film(message.chat.id)
    elif current_chat.one_film_rate == 3:
        if message.text == 'Да':
            film_of_one_film_rate = min_dist_film
            current_chat.one_film_rate = 2
            bot.send_message(message.chat.id, 'Поставьте оценку на появившейся клавиатуре',
                             reply_markup=markups.markup_like_or_not)
        elif message.text == 'Нет':
            Film.create(name=min_dist_film)
            config.MOVIES.append(min_dist_film)
            current_chat.one_film_rate = 2
            bot.send_message(message.chat.id, 'Поставьте оценку на появившейся клавиатуре',
                             reply_markup=markups.markup_like_or_not)
    current_chat.save()


if __name__ == '__main__':
    # init_db()  # При первом запуске раскомментировать
    bot.polling(none_stop=True)
