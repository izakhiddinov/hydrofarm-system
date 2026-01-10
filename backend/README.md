# HydroFarm Backend - Developer Guide

Этот файл предназначен для разработчиков, которые работают с Python backend для HydroFarm.

---

## 1️⃣ Структура папки `backend/`
```
backend/
├── app.py
├── mqtt_client.py
├── db.py
├── config.py
├── gpio.py
├── requirements.txt
└── configs/
    └── template_esp32.json
```

**Примечания:**  
- Все файлы Python находятся здесь.  
- `template_esp32.json` используется для добавления новых ESP32 и сенсоров.  
- Любые изменения фиксируются через GitHub с коммитами.  

---

## 2️⃣ Настройка и запуск Docker (локально или на сервере)

1. Перейти в папку `docker/`.
2. Поднять сервисы:

```bash
docker-compose up -d
```
3. Убедиться, что работают:

    * Mosquitto → mqtt://mosquitto:1883

    * PostgreSQL → postgres:5432

4. Backend автоматически подключается к этим сервисам через переменные окружения в docker-compose.yml.


3️⃣ Работа с template_esp32.json

* Для добавления нового ESP32 модуль:

    1. Сделать копию template_esp32.json.

    2. Изменить device_id на уникальный.

    3. Указать правильные GPIO, I²C адреса и сенсоры.

    4. Сохранить файл в backend/configs/ с уникальным именем (например: esp32_module_02.json).

* JSON файлы backend читает динамически, чтобы новые ESP32 добавлялись без правки кода Python.


4️⃣ Разработка Python кода

* app.py → основной скрипт backend.

* mqtt_client.py → подписка на топики MQTT, получение данных от ESP32.

* db.py → работа с PostgreSQL.

* config.py → глобальные настройки проекта.

* gpio.py → взаимодействие с GPIO Raspberry Pi (если нужно).

5️⃣ Проверка работы
```
python3 app.py
```

* Должны публиковаться данные от ESP32 в MQTT и писаться в PostgreSQL.

* Логи выводятся в консоль.

6️⃣ Добавление новых сенсоров

* Все новые сенсоры добавляются через JSON-конфиг ESP32.

* Backend автоматически подхватывает новые устройства.

* Таблицы подключения в docs/schematics/ нужно обновлять.
