import json
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import requests
from tqdm import tqdm

# Загружаем переменные окружения из файла .env
load_dotenv()

# Класс для формирования ссылки для получения OAuth-токена ВК
class UrlForTokenCreator:
    """
    Класс для создания URL для получения OAuth-токена от ВКонтакте.

    Атрибуты:
    oauth_base_url: str - Базовый URL для запроса токена.
    params: dict - Параметры для создания ссылки авторизации.
    """

    def __init__(self, oauth_base_url=None, params=None):
        """
        Инициализация класса с параметрами по умолчанию, если они не переданы явно.

        Параметры берутся из переменных окружения .env.
        """
        if oauth_base_url is None:
            self.oauth_base_url = os.environ.get('oauth_base_url')

        if params is None:
            self.params = {
                'client_id': os.environ.get('client_id'),
                'display': os.environ.get('display'),
                'redirect_url': os.environ.get('redirect_url'),
                'scope': os.environ.get('scope'),
                'response_type': os.environ.get('response_type'),
                'v': os.environ.get('v'),
                'state':os.environ.get('state')
            }

    def create_url(self):
        """
        Формирует ссылку для авторизации и получения OAuth-токена.

        Возвращает:
        str: Готовая ссылка для авторизации ВКонтакте.
        """
        return f'Перейдите по ссылке: {self.oauth_base_url}?{urlencode(self.params)},{'\n'}авторизуйтесь в ВК и сохраните полученный токен'

# Класс для работы с API ВКонтакте
class ApiVK:
    """
    Класс для взаимодействия с API ВКонтакте.

    Атрибуты:
    request_url: str - Базовый URL для запросов к API ВКонтакте.
    v: str - Версия ВКонтакте.
    owner_id: str - Идентификатор пользователя ВКонтакте.
    token: str - OAuth-токен для доступа к API.
    """
    request_url = 'https://api.vk.com/method'
    v = os.environ.get('v')

    def __init__(self):
        """
        Инициализация объекта ApiVK. Пользователь должен вручную ввести ID своей страницы и OAuth-токен.
        """
        # self.owner_id = os.environ.get('owner_id')
        self.owner_id = input('Введите ID своеЙ страницы: ')

        self.token = input('Введите полученный токен: ')
        # Можно сделать альтернативно: добавить id страницы в .env и читать его оттуда. В контексте данной программы
        # .env выкладывается в публичный репозиторий, т.к. в нем нет никаких приватных данных

    def create_common_params(self):
        """
        Создает общие параметры для API-запросов ВКонтакте.

        Возвращает:
        dict: Общие параметры запроса, такие как токен, версия ВК и id аккаунта пользователя.
        """
        return {
            'access_token': self.token,
            'v': self.v,
            'owner_id': self.owner_id
        }

    def get_photos_list(self):
        """
        Получает список фотографий с профиля пользователя ВКонтакте.

        Сохраняет список фотографий в формате JSON в файл 'info_json.json'.

        Возвращает:
        list: Список фотографий с профиля.
        """
        params = self.create_common_params()
        params.update({
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'

        })
        response = requests.get(f'{self.request_url}/photos.get', params=params)
        data = response.json()

        photos_list = []
        for el in tqdm(data['response']['items']):
            size_info_w = next((el_ for el_ in el['sizes'] if el_['type'] == 'w'), None) # Проверяем, есть ли в данных
            # размер 'w' (самый большой). Если его нет, возвращаем None и переходим к проверке размера 'z'. По умолчанию
            # принимаем, что размер 'z' возвращается всегда
            size_info_z = next((el_ for el_ in el['sizes'] if el_['type'] == 'z'), None)

            size_info = size_info_w if size_info_w is not None else size_info_z

            if size_info is not None:
                if el['likes']['count'] not in photos_list:
                    photos_list.append({
                        el['likes']['count']: [size_info['url'], el['date'], size_info['type']]
                    })
                else:
                    photos_list.append({
                        f'{el['likes']['count']}_{el['date']}': [size_info['url'], size_info['type']]
                    })

        data_for_json = [] # Пишем требуемую структуру данных в json, для этого формируем список, который содержит необходимую
        # структуру
        for photo in tqdm(photos_list):
           for photo_name, photo_data in tqdm(photo.items()):
               data_for_json.append({
                   'file_name': f'{photo_name}.jpg',
                   'size': photo_data[-1]
               })
        with open ('info_json.json', 'w', encoding='utf-8') as file:
            json.dump(data_for_json, file, ensure_ascii=False, indent=2)

        return photos_list

# Класс для работы с API Яндекс.Диск
class ApiYandex:
    """
    Класс для работы с API ЯндексДиска.

    Атрибуты:
    request_url: str - Базовый URL для работы с API ЯндексДиска.
    token: str - OAuth-токен для доступа к ЯндексДиску.
    """
    request_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self):
        self.token = input('Введите свой токен для ЯндексДиска: ')

    def create_common_headers(self):
        """
        Создает общие заголовки для запросов к API Яндекс.Диска.

        Возвращает:
        dict: Заголовки с авторизацией.
        """
        return {
            'Authorization': self.token
        }

    def create_folder(self, directory):
        """
        Создает папку на ЯндексДиске, если она еще не существует.

        Параметры:
        directory: str - Название папки.

        Возвращает:
        str: Название папки.
        """
        params = {
            'path': directory
        }

        # Сперва используем метод, который позволяет получить информацию о папке по указанному пути
        response = requests.get(f'{self.request_url}', params=params, headers=self.create_common_headers())
        folder_data = response.json()
        # Если такая папка есть, в ответе, форматированном в json должен быть ключ '_embedded'. Если такой ключ
        # найден в ответе, то не делаем ничего - папка есть. В противном случае - если нет такого ключа, а
        # значит и папки - создаем папку.
        if '_embedded' in folder_data:
            pass
        else:
            requests.put(f'{self.request_url}', params=params, headers=self.create_common_headers())

        return directory

    def upload_to_disk(self, vk_obj):
        """
        Загружает фотографии с профиля ВКонтакте на ЯндексДиск.

        Параметры:
        vk_obj: ApiVK - Объект класса ApiVK для получения фотографий с ВКонтакте.
        """
        photos_list = vk_obj.get_photos_list()

        for photo in tqdm(photos_list):
            for photo_name, photo_data in tqdm(photo.items()):
                path_to_upload =f'{self.create_folder('downloaded_from_vk')}/{photo_name}.jpg'
                params = {
                    'path': path_to_upload,
                    'url': photo_data[0],
                }
                requests.post(f'{self.request_url}/upload', headers=self.create_common_headers(), params=params)




