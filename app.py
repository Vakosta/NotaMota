import telebot

import config
import markups
import utils
from model import *

current_chat = None

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

film_of_one_film_rate = None
min_dist_film = ''


@bot.message_handler(commands=['start'])
def start(message):
    global current_chat

    try:
        current_chat = Chat.create(id=message.chat.id, rating_stage=True)
    except IntegrityError:
        Chat.get(Chat.id == message.chat.id).delete_instance()
        start(message)
        return

    bot.send_message(message.chat.id, config.MOVIES[0], reply_markup=markups.markup_like_or_not_or_not_watched)
    current_chat.current_film = config.MOVIES[0]
    current_chat.save()


@bot.message_handler(commands=['rate'])
def rate_one_film(message):
    current_chat = Chat.get(Chat.id == message.chat.id)
    current_chat.rate_one_film = 1

    bot.send_message(message.chat.id, 'Введите называние фильма')


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
            current_chat.step += 1
        elif message.text == 'Нейтрально':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=2)
            current_chat.step += 1
        elif message.text == 'Не нравится':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=1)
            current_chat.step += 1
        elif message.text == 'Не смотрел':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=0)

        film = MOVIES[current_chat.step]
        bot.send_message(message.chat.id, film, reply_markup=markups.markup_like_or_not_or_not_watched)
        current_chat.current_film = config.MOVIES[current_chat.step]
        current_chat.save()
    elif current_chat.one_film_rate == 1:
        min_dist = 100000000
        for i in config.MOVIES:
            dist = utils.distance(i.lower(), message.text)
            if dist == 0:
                film_of_one_film_rate = i
                current_chat.one_film_rate = 2
                bot.send_message(message.chat.id, 'Поставьте оценку на появившейся клавиатуре',
                                 reply_markup=markups.markup_like_or_not)
                return
            else:
                min_dist = min(min_dist, dist)
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


if __name__ == '__main__':
    init_db()  # При первом запуске раскомментировать
    bot.polling(none_stop=True)
