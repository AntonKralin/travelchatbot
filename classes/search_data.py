from dataclasses import dataclass, field
from datetime import date, datetime
from classes.models import TableCommand
import decorators


@dataclass
class SearchHotel:
    """
    Класс хранящий данные для запроса
    city: str - город где будет проводиться поиск
    count: int - количество отелей которые необходимо вывести в результате
    foto: bool - необходимо ли загружать фото
    foto_count: int - количество загружаемых фото
    price_start: int - диапазон начала цен
    price_stop: int - диапазон окончания цен
    distance_start: int - диапазон начала цен
    distance_stop: int - диапазон окончания цен
    """

    city: str = ""
    count: int = 0
    day: date = field(default_factory=lambda: datetime.now().date())
    day_count: int = 0
    foto: bool = False
    foto_count: int = 0
    search: str = ""
    price_start: int = 0
    price_stop: int = 0
    distance_start: int = 0
    distance_stop: int = 0

    @decorators.log_decorator
    def save_data(self, id_user: int) -> TableCommand:
        """
        сохранение данных в базу данных
        :param id_user:int уникальный идентификатор пользователя
        :rtype TableCommand
        """
        table = TableCommand()
        table.id_user = id_user
        table.city = self.city
        table.count = self.count
        table.day = self.day
        table.day_count = self.day_count
        table.foto = self.foto
        table.foto_count = self.foto_count
        table.command = self.search
        table.price_start = self.price_start
        table.price_stop = self.price_stop
        table.distance_start = self.distance_start
        table.distance_stop = self.distance_stop
        table.save()
        return table
