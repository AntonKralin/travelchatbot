TOKEN = '5364637571:AAFC2UE9bY9uXZcDfEtrASo09OuVCIFqmrI'

dict_commands = {'/start': 'Проверка работоспособности бота',
                 '/hello_world': 'Hello World',
                 '/help': 'Помощь по боту',
                 '/lowprice': 'Топ дешевых отелей',
                 '/highprice': 'Топ дорогих отелей',
                 '/bestdeal': 'Топ отелей по цене и расположению',
                 '/history': 'История поиска отелей'}

URL_API_ID = "https://hotels4.p.rapidapi.com/locations/v2/search"
URL_API_LIST = "https://hotels4.p.rapidapi.com/properties/list"
URL_API_PHOTO = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
Headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "aa8dc2332fmsh40e2dc77b3e4f2dp1b3298jsne4cbdf1761ab"
}

DB_FILE_NAME = 'history.db'
