from telebot import types
from loadservice import bot
import peewee
from classes.search_data import SearchHotel
from datetime import date, datetime
from classes.hotel_api import HotelsAPI
from classes.enums import CommandsState
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from classes.enums import CommandsLabel
from classes.models import TableState
import decorators


dict_hotel = dict()


def ask_data(message: types.Message, search: str):
    """
    Начало опроса для получния информации
    :param message:
    :param search: откуда вызывается
    :return:
    """
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    search_hotel.search = search
    dict_hotel[message.chat.id] = search_hotel
    try:
        t_state = TableState.get(TableState.id == message.chat.id)
        t_state.state = CommandsState.city.value
        t_state.save()
    except peewee.DoesNotExist:
        t_state = TableState(id=message.chat.id, state=CommandsState.city.value)
        t_state.save(force_insert=True)

    bot.send_message(message.chat.id, 'Введите город для поиска')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.city.value)
@decorators.value_decorator
def get_city(message: types.Message):
    """
    Получаем город
    :param message:
    """
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    city = message.text
    search_hotel.city = city
    dict_hotel[message.chat.id] = search_hotel
    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.count.value
    t_state.save()
    bot.send_message(message.chat.id, 'Введите количество выводимых отелей')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.count.value)
@decorators.value_decorator
def get_count(message: types.Message):
    """
    Получаем количество выводимых отелей
    :param message:
    :return:
    """
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    count = message.text
    count = int(count)
    search_hotel.count = count

    bot.send_message(message.chat.id, 'Дата заезда(YYYY-MM-DD)')
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)
    dict_hotel[message.chat.id] = search_hotel


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    search_hotel = dict_hotel.get(c.message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        search_hotel.day = result
        bot.edit_message_text(result,
                              c.message.chat.id,
                              c.message.message_id)
        t_state = TableState.get(TableState.id == c.message.chat.id)
        t_state.state = CommandsState.day_count.value
        t_state.save()
        dict_hotel[c.message.chat.id] = search_hotel
        bot.send_message(c.message.chat.id, ' Количество дней пребывания')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.day_count.value)
@decorators.value_decorator
def get_day_count(message: types.Message):
    """
    Получаем количество дней пребывания
    :param message:
    :return:
    """
    day_count = message.text
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()

    day_count = int(day_count)
    search_hotel.day_count = day_count

    dict_hotel[message.chat.id] = search_hotel
    if search_hotel.search != CommandsLabel.bestdeal.value:
        t_state = TableState.get(TableState.id == message.chat.id)
        t_state.state = CommandsState.foto.value
        t_state.save()
        button = yes_no_button()
        bot.send_message(message.chat.id, 'Нужны ли фото да/нет', reply_markup=button)
    else:
        t_state = TableState.get(TableState.id == message.chat.id)
        t_state.state = CommandsState.price_start.value
        t_state.save()
        bot.send_message(message.chat.id, 'Диапазон цен от(USD)')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.price_start.value)
@decorators.value_decorator
def get_price_start(message: types.Message):
    start = message.text

    start = int(start)
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    search_hotel.price_start = start
    dict_hotel[message.chat.id] = search_hotel
    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.price_stop.value
    t_state.save()
    bot.send_message(message.chat.id, 'Диапазон цен до(USD)')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.price_stop.value)
@decorators.value_decorator
def get_price_stop(message: types.Message):
    stop = message.text

    stop = int(stop)
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    search_hotel.price_stop = stop
    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.distance_start.value
    t_state.save()
    bot.send_message(message.chat.id, 'Диапазон расстояний от(Миль)')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.distance_start.value)
@decorators.value_decorator
def get_distance_start(message: types.Message):
    start = message.text

    start = int(start)
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    search_hotel.distance_start = start
    dict_hotel[message.chat.id] = search_hotel
    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.distance_stop.value
    t_state.save()
    bot.send_message(message.chat.id, 'Диапазон расстояний до(Миль)')


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.distance_stop.value)
@decorators.value_decorator
def get_distance_stop(message: types.Message):
    stop = message.text

    stop = int(stop)
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    search_hotel.distance_stop = stop

    button = yes_no_button()
    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.foto.value
    t_state.save()
    bot.send_message(message.chat.id, 'Нужны ли фото да/нет', reply_markup=button)


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.foto.value)
def get_foto(message: types.Message):
    """
    Получаем необходимость в фото. Если не нужны выводим инфу по отелям
    :param message:
    :return:
    """
    foto = message.text
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    if foto.lower() == 'да':
        search_hotel.foto = True
        bot.send_message(message.chat.id, 'Введите количество фото', reply_markup=types.ReplyKeyboardRemove())
        t_state = TableState.get(TableState.id == message.chat.id)
        t_state.state = CommandsState.foto_count.value
        t_state.save()
        dict_hotel[message.chat.id] = search_hotel
    else:
        t_state = TableState.get(TableState.id == message.chat.id)
        t_state.state = CommandsState.stop.value
        t_state.save()
        search_hotel.foto = False
        hotel_api = HotelsAPI()
        hotel_api.get_hotels_by_search(search_hotel)
        print_hotel(message, hotel_api)


@bot.message_handler(func=lambda message: TableState.get_state(message.chat.id) == CommandsState.foto_count.value)
@decorators.value_decorator
def get_foto_count(message: types.Message):
    """
    Получаем количество фото и выводим инфу по отелям
    :param message:
    :return:
    """
    foto_count = message.text
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()

    foto_count = int(foto_count)
    search_hotel.foto_count = foto_count

    t_state = TableState.get(TableState.id == message.chat.id)
    t_state.state = CommandsState.stop.value
    t_state.save()

    hotel_api = HotelsAPI()
    hotel_api.get_hotels_by_search(search_hotel)
    print_hotel(message, hotel_api, True, foto_count)
    dict_hotel[message.chat.id] = search_hotel


@decorators.log_decorator
def print_hotel(message: types.Message, hotels_api: HotelsAPI, foto: bool = False, foto_count: int = 5):
    """
    вывод инфы по отелям в телеграм
    :param message:
    :param hotels_api: обьект для работы с отелями
    :param foto: bool - нужны ли фото
    :param foto_count: int - количество фото
    :return:
    """
    bot.send_chat_action(message.chat.id, 'typing')
    photo_dict = dict()
    search_hotel = dict_hotel.get(message.chat.id)
    if not search_hotel:
        search_hotel = SearchHotel()
    if foto is True:
        photo_dict = hotels_api.get_photo_dict(foto_count)
    table_command = search_hotel.save_data(message.from_user.id)
    for i_hotel in hotels_api.hotels:
        text = "Название: " + i_hotel.name + "\n"
        text += "Адресс: " + i_hotel.address + "\n"
        text += "Расстояние от " + i_hotel.label_distance + ": " + i_hotel.centr_distance + "\n"
        text += "Цена за один день: " + i_hotel.price + '\n'
        price = i_hotel.price.replace('$', '')
        try:
            price = price.replace(',', '')
            price = int(price)
            all_price = search_hotel.day_count * price
        except ValueError:
            all_price = 0
        text += 'Цена за {}: {}$'.format(search_hotel.day_count, all_price) + '\n'
        text += "Cсылка на отель: https://www.hotels.com/ho" + i_hotel.s_id
        i_hotel.save_data(table_command)
        bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove(), disable_web_page_preview=True)

        if foto is True and photo_dict:
            media_list = []
            for i_photo in photo_dict[i_hotel.s_id]:
                media_list.append(types.InputMediaPhoto(i_photo))
            if len(media_list) != 0:
                try:
                    bot.send_media_group(message.chat.id, media=media_list)
                except Exception as excp:
                    print(excp)

    bot.send_message(message.chat.id, 'Введите команду. /help - помощь по командам')


def yes_no_button() -> types.ReplyKeyboardMarkup:
    button = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Да")
    item2 = types.KeyboardButton("Нет")
    button.add(item1)
    button.add(item2)
    return button
