# HydroFarm Developer Contract

### 🗄️ Структура Данных (Модель DeviceConfig)

Каждое устройство в базе — это JSON-объект:
{
  "id": "строка (уникальный ID)",
  "device_type": "pump / valve / light / fan",
  "label": "Красивое имя для сайта",
  "connection_type": "relay (реле) или modbus (инвертор)",
  "pin_number": "число (номер GPIO)",
  "modbus_address": "число (для инверторов)",
  "status": "online / offline"
}

### 🚀 Порядок разработки (Workflow)
1. **Backend:** Описывает таблицы в `models.py`.
2. **Frontend:** Делает `fetch()` к API.
3. **Agent:** Читает API и крутит моторы.



## 1️⃣ Структура проекта на GitHub

**Проект на GitHub:** `hydrofarm-system`

```
hydrofarm-system/
├── backend/
│   ├── app/
│   	├── models.py
│   ├── configs/
│   	├── template_esp32.json
│   ├── Dockerfile
│   ├── README.md
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── gpio.py
│   ├── main.py
│   ├── mqtt_client.py
│   ├── requirements.txt
├── devices/
│   	├── rpi_agent.py
│ 
└── docker/
│   ├── mosquito/
│   	├── README.md
│   	├── mosquitto.conf
│   ├── postgres/
│   	├── README.md
│   	├── init.sql
│   	├── pg_hba.conf
│   	├── postgresql.conf
│   ├── README.md
│   ├── docker-compose.yml
│   ├── mosquitto.conf
└── docs/
│   ├── contracts/
│   	├── developer_contract.md
│   ├── manuals/
│   	├── .gitkeep
│   ├── schematic/
│   	├── hydrofarm_connections Vers_01.pdf
│   	├── hydrofarm_connections Vers_01.vsdx
└── esp32/
│   ├── common/
│   	├── README.md
│   ├── esp32_module_01/
│   	├── README.md
│   	├── config.h
│   	├── esp32_module_01.ino
│   ├── README.md
└── tools/
│   ├── test_mqtt.py
└── web/
│   ├── README.md
│   ├── index.html
└── .gitignore
└── LICENSE
└── README.md
```
