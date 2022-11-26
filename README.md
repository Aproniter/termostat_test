# thermostat_test
thermostat

<h1 align="center">Провайдер управления термостатом с возможностью интеграции в Yandex Smart Home</h1>


### Технологии
Python 3.11
FastApi 0.87.0
SQLAlchemy 1.4.41
databases 0.6.2


### Запуск проекта в dev-режиме
- В главной папке запустите uvicorn сервер с fastapi:
    - uvicorn main:app --reload

### Description
Сервис для управления устройствами пользователя, с возможностью подключения голосового управления через сервисы Яндекс Алисы.

**API**
Подробная документация доступна по адресу localhost/docs/