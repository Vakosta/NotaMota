DATABASE_DATA = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd55juqn67jac81',
    'USER': 'ildwfawbdhxfbs',
    'PASSWORD': '2fa2d45e7c6f6b6b9dbd92d5a34d35225858573baacf0782599bbd5ad3c62f65',
    'HOST': 'ec2-54-75-227-92.eu-west-1.compute.amazonaws.com',
    'PORT': '5432',
}

TELEGRAM_TOKEN = '517628481:AAFxaQ9aqzJiweOQdMMKNRaLJ9Y5OUMKa38'

MOVIES = ['Звёздные войны: последний джедай', 'Рик и Морти', 'Защитники',
          'Пираты Карибского моря', 'Тайна Коко', 'Железный человек',
          'Эмоджи фильм', 'Во все тяжкие', 'Шерлок', 'Кухня', 'Титаник',
          'Гравити фолз', 'Джентльмены удачи', '1+1', 'Гарри Поттер',
          'Отряд самоубийц', 'Фантастические твари и где они обитают',
          'Мстители', 'Марсианин', 'Залечь на дно в Брюгге', 'Интерстеллар',
          'Крым', 'Криминальное чтиво', 'Стражи галактики', 'Хардкор',
          'Дэдпул', 'Зелёная миля', 'Омерзительная восьмёрка',
          'Крёстный отец', 'Побег из Шоушенка', 'Оно', 'Игра престолов',
          'Волк с Уолл-стрит', 'Великий Гэтсби', 'Иллюзия обмана',
          'Выживший', 'Взломать блогеров', 'Начало', 'Огненный путь',
          'Изгой 1. Звёздные войны: истории', 'Волшебники', 'Одиссея',
          'Вспомнить всё', 'Остаться в живых', 'Иллюзионист',
          'Три билборда на границе Эббинга, Миссури', 'Демоны да Винчи',
          'Восьмая миля', 'С любовью, Винсент', 'Чёрное зеркало',
          'Странные дела', 'Безумный Макс', 'Властелин колец', 'День сурка',
          'Римские каникулы', 'Красотка', 'Назад в будущее', 'Летят журавли',
          'Зеркало', 'Андрей Рублев', 'Солярис',
          'Двенадцать разгневанных мужчин', 'Кингсман', 'Лобстер', 'Фарго',
          'Листопад', 'И гаснет свет', 'Ривердэйл', 'Повелитель времени',
          'Голубая бездна', 'Эдвард руки-ножницы', 'Беги, Лола, беги',
          'КРиминальное чтиво', 'Хоббит', 'Страх и ненависть в Лас-Вегасе',
          'День выборов', 'Сплит', 'Аватар', 'Зверополис',
          'Меч короля Артура', 'Головоломка', 'Хроники Риддика', 'Рэд',
          'Рапунцель', 'Агенты U.N.C.L.E.', 'Приключения Паддингтона',
          'Иван Васильевич меняет профессию', 'Территория', 'Престиж',
          'Потрошитель', 'Всегда говори ДА', 'Отпуск по обмену',
          'Изгой-1. Звёздные войны: истории', 'Ривердейл',
          'Джентельмены удачи', 'Любить', 'Настоящий детектив',
          'Город героев', 'Песнь моря', 'Восьмое чувство',
          'Портрет Дориана Грея', 'Как избежать наказания за убийство',
          'Защитники ', 'Джентльмены удачи ', 'Большой Лебовски',
          'Кавказская пленница', 'Омерзительная восьмерка''Собачий полдень',
          'Оз: Великий и ужасный', 'Унесенные прихзраками', 'Тупой и еще тупее',
          'Неуловимые',
          'Очень страшное кино',
          'Экзамен для двоих',
          'Университет монстров',
          'Тихоокеанский рубеж',
          'Турбо',
          'Смурфики',
          'Элизиум - не рай на земле',
          'Два ствола',
          'Астрал',
          'Игра Эндера',
          'Тор',
          'Холодное сердце',
          'Ку! Кин-дза-дза',
          'Чужие',
          'Я легенда',
          'Судный День',
          'Золото дураков',
          'Бугимен',
          'ВАЛЛ-И',
          'Темный рыцарь',
          'На краю рая',
          'Вольт',
          'День, когда Земля остановилась',
          'Самый лучший фильм',
          'Индиго', 'День Радио',
          'Реальный Папа',
          'Игра',
          'Мираж',
          'Гитлер капут!',
          'Новая земля',
          'Приключения Алёнушки и Ерёмы',
          'Морфий',
          'Стиляги',
          'Экипаж',
          'Книга Джунглей',
          'Выживший',
          'Лес призраков',
          'Дедушка легкого поведения',
          'Кукла',
          '50 оттенков черного',
          'Запретная зона',
          '8 лучших свиданий',
          'Вирус',
          'СуперБобровы',
          'Экстрасенсы',
          'Раскол',
          'Левиафан',
          'Ледниковый период',
          'Азазель',
          'Дети шпионов',
          'Коробка',
          'Высотка',
          'Робинзон Крузо: Очень обитаемый остров',
          'Варкрафт',
          'Финансовый монстр',
          'Славные парни',
          'Кто подставил кролика Роджера?',
          'Мобильник',
          'Коралина в стране кошмаров',
          'Диггеры',
          'Полный расколбас', 'Зеленый слоник']
