import logging
from functools import wraps
from loadservice import bot


def value_decorator(func):
    """
    декоратор обработки ошибки введенных данных
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rez = func(*args, **kwargs)
            return rez
        except ValueError:
            bot.send_message(args[0].chat.id, "Ошибка ввода")
    return wrapper


def log_decorator(func):
    """
    декоратор логирования ошибок
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.basicConfig(filename='myapp.log', format='%(asctime)s %(message)s', level=logging.INFO)
        try:
            rez = func(*args, **kwargs)
            return rez
        except Exception as exc:
            logging.warning(exc, func)

    return wrapper
