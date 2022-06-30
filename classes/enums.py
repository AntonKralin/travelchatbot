from enum import Enum


class CommandsLabel(Enum):
    lowprice = 'lowprice'
    highprice = 'highprice'
    bestdeal = 'bestdeal'
    history = 'history'


class CommandsState(Enum):
    city = 'city'
    count = 'count'
    day = 'day'
    day_count = 'day_count'
    foto = 'foto'
    foto_count = 'foto_count'
    price_start = 'price_start'
    price_stop = 'price_stop'
    distance_start = 'distance_start'
    distance_stop = 'distance_stop'
    stop = 'stop'
