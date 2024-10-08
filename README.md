# Резервное копирование фотографий со страницы ВК на ЯндексДиск

___Программа использует API Вконтакте для выгрузки фотографий с аватара ВК и сохраняет их в отдельно созданную папку на ЯндексДиске.
Требования, которым удовлетворяет программа, подробно описаны по ссылке [https://github.com/netology-code/py-diplom-basic](https://github.com/netology-code/py-diplom-basic)
 Программа написана в учебных целях, а также для портфолио, чтобы продемонстрировать потенциальному работодателю навыки работы с OpenAPI, ООП и используемыми в программе библиотеками.___

Примечания:

- Первое, что может броситься в глаза: репозиторий содержит файл .env. Однако в нем нет никаких приватных данных, и используется он только для чтения переменных. Дополнительные пояснения есть в самом коде в виде комментариев.
- Используемые классы задукоментированы по правилам составления документации в коде.
- Список всех зависимостей проекта находится в requirments.txt
- Классы и логика инкапсулированы в отдельном .py-файле. Исполняемый файл содержит импорт классов и вызов методов.
- Приложение требует авторизации ВК под вашим логином и паролем. Приложение имеет доступ *только* к фото ВК.
- Сохранение фото на ЯД происходит по url фотографий, которые необходимо загрузить. Таким образом не требуется программно скачивать фотографии и хранить их на сервере клиента, где запущено приложение.
