from vk_yandex_api import UrlForTokenCreator, ApiVK, ApiYandex

if __name__ == '__main__':
    # Создание ссылки для получения токена ВКонтакте
    url_creator = UrlForTokenCreator()
    print(url_creator.create_url())

    # Получение фотографий с профиля ВКонтакте и загрузка на Яндекс.Диск
    vk_obj = ApiVK()
    yandex_obj = ApiYandex()
    yandex_obj.upload_to_disk(vk_obj)