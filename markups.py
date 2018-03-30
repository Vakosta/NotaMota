from telebot import types

markup_like_or_not_or_not_watched = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup_like_or_not_or_not_watched.add('Нравится')
markup_like_or_not_or_not_watched.add('Не смотрел')
markup_like_or_not_or_not_watched.add('Не нравится')
markup_like_or_not_or_not_watched.add('Нейтрально')

markup_like_or_not = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup_like_or_not.add('Нравится')
markup_like_or_not.add('Не нравится')
markup_like_or_not.add('Нейтрально')

markup_yes_or_no = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup_yes_or_no.add('Да')
markup_yes_or_no.add('Нет')
