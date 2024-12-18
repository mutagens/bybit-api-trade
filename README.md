# Bybit Trading Bot

Этот скрипт представляет собой торгового бота для платформы **Bybit**, который позволяет взаимодействовать с API Bybit для размещения ордеров (маркет и лимитных), получения баланса и сохранения истории ордеров.

## Описание

На данный момент бот использует API Bybit для работы с учетными записями и ордерами. Он поддерживает следующие функции:
- Размещение маркет-ордера для покупки и продажи.
- Размещение лимитного ордера для покупки и продажи.
- Получение баланса по учетной записи.
- Логирование событий в файл с помощью логгера.
- Сохранение истории ордеров в json файл.


## Требования

Для запуска бота необходимо установить следующие зависимости:
- Python 3.8 и выше
- Библиотеки:
  - `pybit` — для взаимодействия с API Bybit
  - `requests` — для работы с HTTP-запросами (возможно, уже включен в вашу среду)
  - `logging` — для логирования
  - `json` — для сохранения истории ордеров в файл
  - `os` — для работы с файловой системой

Для более удобной установки всех зависимостей можете прописать pip freeze > requirements.txt

Дальше просто pip install requirements


  
