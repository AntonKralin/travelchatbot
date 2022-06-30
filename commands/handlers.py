from telebot import TeleBot, types
from loadservice import bot
import config
import commands.universal as universal
from classes.models import TableCommand, TableHotel
from classes.enums import CommandsLabel
import decorators


@bot.message_handler(commands=['help'])
def process(message: types.Message):
    """Обработка команды /help"""
    text = ''
    for i_key, i_value in config.dict_commands.items():
        text += i_value + ' - ' + i_key + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def handler_start(message: types.Message):
    """Обработка команды /start"""
    start_message = "Привет. Я бот для туристической фирмы. Для помощи введите /help"
    bot.send_message(message.chat.id, start_message)


@bot.message_handler(commands=['hello_world'])
def handler_start(message: types.Message):
    """Обработка команды /hello_world"""
    bot.send_message(message.chat.id, 'Hello World')


@bot.message_handler(commands=['lowprice'])
def lowprice(message: types.Message):
    universal.ask_data(message, search=CommandsLabel.lowprice.value)


@bot.message_handler(commands=['highprice'])
def highprice(message: types.Message):
    universal.ask_data(message, search=CommandsLabel.highprice.value)


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: types.Message):
    universal.ask_data(message, search=CommandsLabel.bestdeal.value)


@decorators.log_decorator
@bot.message_handler(commands=['history'])
def history(message: types.Message):
    """
    Обрабатываем команду history
    :param message:
    """
    id_user = message.from_user.id
    m_command = TableCommand.select().where(TableCommand.id_user == id_user).order_by(TableCommand.id.desc()).limit(5)
    if len(m_command) == 0:
        bot.send_message(message.chat.id, 'Вы еще не делали никаких запросов')
    else:
        for i_command in m_command:
            text = "{date} <b>{command}</b> город: <b>{city}</b> количество отелей: <b>{count}</b> " \
                   "день заезда <b>{day_in}</b> количество дней пребывания <b>{day_count}</b> ".format(
                                                                                              date=i_command.created_at,
                                                                                              command=i_command.command,
                                                                                              city=i_command.city,
                                                                                              count=i_command.count,
                                                                                              day_in=i_command.day,
                                                                                              day_count=i_command.day_count)
            if i_command.foto is True:
                text += ' загружать фото: <b>да</b> количество фото: <b>{}</b> '.format(i_command.foto_count)
            else:
                text += 'загружать фото: <b>нет</b> '
            if i_command.command == 'bestdeal':
                text += 'цена от <b>{start}</b> до <b>{stop}</b> '.format(start=i_command.price_start,
                                                                          stop=i_command.price_stop)
                text += 'расстояние от <b>{start} до </b>{stop} '.format(start=i_command.distance_start,
                                                                         stop=i_command.distance_stop)
            bot.send_message(message.chat.id, text, parse_mode='html')
            find_hotels = TableHotel.select().where(TableHotel.command == i_command)
            bot.send_message(message.chat.id, 'Найденные отели:')
            for i_hotel in find_hotels:
                text_hotel = 'название: <b>{name}</b> адресс: <b>{address}</b> ' \
                             'цена за один день <b>{price}</b>'.format(name=i_hotel.name, address=i_hotel.address,
                                                                       price=i_hotel.price)
                bot.send_message(message.chat.id, text_hotel, parse_mode='html')
        bot.send_message(message.chat.id, 'Введите команду. /help - помощь по командам')
