import telebot
import config
import markups
import recommendations.candidates as candidates
import utils
from model import *
from random import random, sample

current_chat = None

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

film_of_one_film_rate = None
min_dist_film = ''

films_for_user = {}
messages = {}


def get_actions():
    actions = list(Action.select().execute())

    result = {}
    for i in actions:
        if i.rating > 0:
            result[(i.chat_id, i.film)] = i.rating

    return result


def select_film(user):
    global films_for_user

    pairs = sample(films_for_user[user].items(), k=len(films_for_user[user]))

    cumsums = [(None, 0)]
    for movie, rating in pairs:
        cumsums.append((movie, cumsums[-1][1] + rating))

    ind = (cumsums[-1][1] + 1) * random()
    movie_to_pop = None
    for i, tup in enumerate(cumsums[1:]):
        if ind >= tup[1]:
            movie_to_pop = cumsums[i - 1][0]
            break

    if movie_to_pop is None:
        movie_to_pop = cumsums[-1][0]

        if movie_to_pop is not None:
            _ = films_for_user[user].pop(movie_to_pop)

    return movie_to_pop


def send_film(id):
    data = get_actions()

    if current_chat.step < 10 or len(data) < 100:
        film = MOVIES[current_chat.step]
        message = 'Оцените фильм, позязя'
    else:
        if id not in films_for_user.keys() or len(films_for_user[id]) == 1:
            films_for_user[id], messages[id] = candidates.get_candidates(get_actions(), id)

        film = select_film(id)
        if film is None:
            return
            # for movie in MOVIES:
            #     if (id, movie) in data.keys():
            #         film = movie
            #         break

        if film in messages[id].keys():
            message = messages[id][film]
        else:
            message = ''

    bot.send_message(id, '\n\n'.join([film, message]), reply_markup=markups.markup_like_or_not_or_not_watched)

    current_chat.current_film = film
    # config.MOVIES[current_chat.step]


@bot.message_handler(commands=['start'])
def start(message):
    global current_chat

    current_chat = Chat.get_or_create(id=message.chat.id)[0]

    send_film(message.chat.id)
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
                          film=current_chat.current_film,
                          rating=True)
        elif message.text == 'Не нравится':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
                          rating=None)
        elif message.text == 'Не смотрел':
            Action.create(chat_id=message.chat.id,
                          film=current_chat.current_film,
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
            film_of_one_film_rate = min_dist_film
            config.MOVIES.append(min_dist_film)
            current_chat.one_film_rate = 2
            bot.send_message(message.chat.id, 'Поставьте оценку на появившейся клавиатуре',
                             reply_markup=markups.markup_like_or_not)
    current_chat.save()


if __name__ == '__main__':
    # init_db()  # При первом запуске раскомментировать
    bot.polling(none_stop=True)
