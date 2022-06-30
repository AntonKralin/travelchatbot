import requests
import config
import json
from datetime import date, datetime, timedelta
from classes.search_data import SearchHotel
from classes.enums import CommandsLabel
from classes.hotel import Hotel
import decorators


class HotelsAPI:
    """
    Класс для работы с rapid
    """
    def __init__(self, locale: str = 'en_US', currency: str = 'USD'):
        self._hotels = list()
        self._locale = locale
        self._currency = currency

    @property
    def hotels(self) -> list:
        return self._hotels

    @decorators.log_decorator
    def get_destination_id(self, search: str, ) -> str:
        """
        ищем id в сайте
        :param search: переменная для поиска
        :return:
        """
        querystring = {"query": search, "locale": self._locale, "currency": self._currency}
        response = requests.request("GET", config.URL_API_ID, headers=config.Headers, params=querystring)
        if response.status_code == requests.codes.ok:
            rez_json = json.loads(response.text)
            destination_id = rez_json['suggestions'][0]['entities'][0]['destinationId']
            return destination_id

    @decorators.log_decorator
    def get_hotels_by_search(self, data: SearchHotel, page_number: int = 1):
        """
        Получаем список отелей
        :param data: SearchHotel данные для поиска
        :param page_number: int страница вывода
        :return: list(Hotel)
        """
        search_name = data.search
        destination_id = self.get_destination_id(data.city)
        if destination_id:
            check_out = data.day + timedelta(days=data.day_count)
            page_size = str(data.count)
            if search_name == CommandsLabel.lowprice.value:
                sort_string = "PRICE"
            elif search_name == CommandsLabel.highprice.value:
                sort_string = "PRICE_HIGHEST_FIRST"
            else:
                sort_string = "DISTANCE_FROM_LANDMARK"
                page_size = '25'
            querystring = {"destinationId": destination_id, "pageNumber": page_number, "pageSize": page_size,
                           "checkIn": str(data.day), "checkOut": str(check_out), "adults1": str(1),
                           "sortOrder": sort_string, "locale": self._locale, "currency": self._currency}
            if search_name == CommandsLabel.bestdeal.value:
                querystring['priceMin'] = data.price_start
                querystring['priceMax'] = data.price_stop
            response = requests.request("GET", config.URL_API_LIST, headers=config.Headers, params=querystring)
            if response.status_code == requests.codes.ok:
                rez_json = json.loads(response.text)
                rez_list = rez_json['data']["body"]['searchResults']['results']
                self._create_hotels_list(rez_list)
                if search_name == CommandsLabel.bestdeal.value:
                    self._upd_bestdeal_result(data.distance_start, data.distance_stop)
                    for i in range(2, 4):
                        if len(self._hotels) == data.count:
                            break
                        elif len(self._hotels) > data.count:
                            self._hotels = self._hotels[:data.count]
                            break
                        else:
                            self.get_hotels_by_search(data, page_number=i)

    @decorators.log_decorator
    def _upd_bestdeal_result(self, start: int, stop: int):
        """
        bestdeal удаление из списка отелей не соответствующих диапазону расстояний
        :param start: стартовая расстояние
        :param stop: конечная конечное расстояние
        """
        hotels = list()
        for i_hotel in self._hotels:
            buf_mass = i_hotel.centr_distance.split(' ')
            distance = 0
            try:
                distance = float(buf_mass[0])
            except ValueError as exc:
                print(exc)
            if (float(start) <= distance) and (float(stop) >= distance):
                hotels.append(i_hotel)
        self._hotels = hotels

    @decorators.log_decorator
    def _create_hotels_list(self, json_list):
        """
        Парсим строку и получаем список отелей
        :param json_list: json строка для парсинга
        :return:
        """
        hotels_list = list()
        for i_elem in json_list:
            hotel = Hotel()
            hotel.s_id = str(i_elem.get("id"))
            buf = i_elem.get('address')
            if buf:
                buf = buf.get('streetAddress')
            if not buf:
                buf = ''
            hotel.address = buf
            hotel.name = i_elem.get('name')
            hotel.star_rating = i_elem.get('starRating')
            buf = i_elem.get('ratePlan')
            if buf:
                buf = buf.get('price')
            if buf:
                buf = buf.get('current')
            if not buf:
                buf = '0'
            hotel.price = buf
            buf = i_elem.get("landmarks")
            if buf:
                buf = buf.pop(0)
            buf1 = None
            buf2 = None
            if buf:
                buf1 = buf.get("distance", "0")
                buf2 = buf.get("label")
            if not buf1:
                buf1 = ''
            if not buf2:
                buf2 = ''
            hotel.centr_distance = buf1
            hotel.label_distance = buf2
            hotels_list.append(hotel)
        self._hotels.extend(hotels_list)

    @decorators.log_decorator
    def get_photo_dict(self, count: int = 5) -> dict:
        """
        Получаем список урл для вывода фото
        :param count: количество фото
        :return:
        """
        photo_dict = dict()
        for i_elem in self._hotels:
            querystring = {"id": i_elem.s_id}
            response = requests.request("GET", config.URL_API_PHOTO, headers=config.Headers, params=querystring)
            if response.status_code == requests.codes.ok:
                rez_json = json.loads(response.text)
                rez_list = rez_json["hotelImages"]
                i_count = 0
                i_list = list()
                for i_photo in rez_list:
                    i_count += 1
                    if i_count > count:
                        break
                    base_url = i_photo["baseUrl"]
                    suffix = i_photo["sizes"][0]["suffix"]
                    base_url = base_url.replace("{size}", suffix)
                    i_list.append(base_url)
                photo_dict[i_elem.s_id] = i_list
        return photo_dict
