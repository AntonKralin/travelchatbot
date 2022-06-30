from dataclasses import dataclass
from classes.models import TableHotel, TableCommand
import decorators


@dataclass
class Hotel:
    """
    Класс представляющий отель
    s_id: id отеля
    name: имя отеля
    star_rating: количество звезд
    address: аддресс отеля
    price: цена за один день
    centr_distance: расстояние от метки
    label_distance: метка для расстояния
    """
    s_id: str = ""
    name: str = ""
    star_rating: str = ""
    address: str = ""
    price: str = ""
    centr_distance: str = ""
    label_distance: str = ""

    @decorators.log_decorator
    def save_data(self, command: TableCommand):
        table_hotel = TableHotel()
        table_hotel.command = command
        table_hotel.name = self.name
        table_hotel.star_rating = self.star_rating
        table_hotel.address = self.address
        table_hotel.price = self.price
        table_hotel.centr_distance = self.centr_distance
        table_hotel.label_distance = self.label_distance
        table_hotel.save()



