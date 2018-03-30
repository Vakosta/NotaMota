from telebot import types

markup_like_or_not_or_not_watched = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
markup_like_or_not_or_not_watched.row('Нравится', 'Нейтрально', 'Не нравится')
markup_like_or_not_or_not_watched.row('Не смотрел')

markup_like_or_not = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
markup_like_or_not.row('Нравится', 'Нейтрально', 'Не нравится')

markup_yes_or_no = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
markup_yes_or_no.row('Да', 'Нет')
