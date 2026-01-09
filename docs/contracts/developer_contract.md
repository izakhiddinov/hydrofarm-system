# HydroFarm Developer Contract

---

## 1️⃣ Структура проекта на GitHub

Проект на GitHub: `hydrofarm-system`
```
hydrofarm-system/
├── backend/   # Python код, обработка MQTT, работа с БД
├── docker/
│   ├── mosquitto/  # конфиг Mosquitto, volume для хранения сообщений
│   └── postgres/   # конфиг PostgreSQL, volume для базы
├── docs/
│   ├── schematics/ # Visio и PDF схемы подключения
│   ├── manuals/    # Руководства
│   └── contracts/  # Контракты и инструкции
├── esp32/    # код для ESP32 и конфиги
├── web/      # HTML, CSS, JS
├── .gitignore
├── LICENSE
└── README.md
```


**Примечания:**

- Все изменения фиксируются через GitHub.
- Каждый новый модуль (ESP32, датчик, насос) добавляется в соответствующую папку и сопровождается документацией в `docs/`.

---

## 2️⃣ Общие правила для разработчиков

1. Все изменения **вносятся через GitHub** с коммитами и описанием.
2. Для крупных изменений используем **ветки (branches)** и pull requests.
3. Каждый разработчик согласовывает новые сенсоры и модули в контракте.
4. Все датчики и устройства должны быть описаны в таблице для Raspberry Pi и ESP32.

---

## 3️⃣ Таблица подключений и устройств

### Raspberry Pi 5 (основной сервер)

#### Таблица для программиста

| №  | GPIO         | Название       | Тип          | Описание                                | Дополнительная инф.                                   | I²C_ADDRESS / Канал |
|----|-------------|----------------|-------------|----------------------------------------|------------------------------------------------------|-------------------|
| 1  | 21          | FLOW_SENSOR_1  | INPUT       | Импульсы расхода воды                  | INPUT, PULSE, 3.3V (ACTIVE LOW)                     | -                 |
| 2  | 26          | INLET_VALVE_1  | OUTPUT      | Клапан подачи воды 12V                 | OUTPUT, RELAY, ACTIVE LOW                            | -                 |
| 3  | 17          | PUMP_1         | OUTPUT      | Насос 1 (основной для подачи)          | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 4  | 27          | PUMP_2         | OUTPUT      | Насос 2 (резервный)                     | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 5  | 5           | PUMP_3         | OUTPUT      | Насос 3 (дозирующий)                   | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 6  | 6           | PUMP_4         | OUTPUT      | Насос 4 (дозирующий)                   | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 7  | 13          | PUMP_5         | OUTPUT      | Насос 5 (дозирующий)                   | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 8  | 19          | PUMP_6         | OUTPUT      | Насос 6 (дозирующий)                   | OUTPUT, RELAY, ACTIVE LOW (5V->12V->Motor)          | -                 |
| 9  | 22          | LIGHT_1        | OUTPUT      | Свет                                   | RELAY, 5V, ACTIVE LOW                                | -                 |
| 10 | 23          | FAN_1          | OUTPUT      | Вентиляторы                             | RELAY, 5V, ACTIVE LOW                                | -                 |
| 11 | 24          | FILL_VALVE_2   | OUTPUT      | Клапан долива                           | RELAY, 5V, ACTIVE LOW                                | -                 |
| 12 | A0 (ADS1115) | PH_SENSOR_1    | ANALOG_INPUT| pH-датчик через делитель 10k/10k       | ADC ×2 для реального значения                        | 0x48 / A0         |
| 13 | A1 (ADS1115) | TDS_SENSOR_1   | ANALOG_INPUT| TDS-датчик через делитель 10k/10k      | ADC ×2 для реального значения                        | 0x48 / A1         |
| 14 | A2 (ADS1115) | RESERVED_2     | ANALOG_INPUT| Резервный                                | Для будущих аналоговых датчиков                       | 0x48 / A2         |
| 15 | A3 (ADS1115) | RESERVED_3     | ANALOG_INPUT| Резервный                                | Для будущих аналоговых датчиков                       | 0x48 / A3         |
| 16 | 4           | WATER_TEMP_1   | INPUT       | Температура воды (DS18B20, 1-Wire)    | Подтяжка 4.7kΩ, питание 3.3V AMS1117               | -                 |
| 17 | 18          | ULTRASONIC_TRIG_1 | OUTPUT   | УЗ датчик уровня (Trig)                | OUTPUT, 3.3V, 1 GPIO на Trig                         | -                 |
| 18 | 25          | ULTRASONIC_ECHO_1 | INPUT    | УЗ датчик уровня (Echo)                | INPUT, 5V → 3.3V делитель, 1 GPIO на Echo           | -                 |

---

### ESP32 (модули для масштабирования)

#### Таблица для программиста ESP32

| №  | GPIO | Название           | Тип           | Описание                                | Дополнительная инф.                                               | I²C_ADDRESS / Канал |
|----|------|------------------|---------------|----------------------------------------|------------------------------------------------------------------|-------------------|
| 1  | 21   | CO2/VOC_1        | I²C           | CO₂ / VOC                               | SDA → GPIO21, SCL → GPIO22, питание 3.3V от AMS1117, GND общая  | 0x5A              |
| 2  | 22   | illumination_1   | I²C           | Освещённость                            | SDA → GPIO21, SCL → GPIO22, питание 3.3V от AMS1117, GND общая  | 0x23              |
| 3  | 4    | temp_humidity_1  | DIGITAL_INPUT | Температура и влажность воздуха         | DATA → GPIO4, резистор 10kΩ между DATA и VCC, питание 3.3V AMS1117 | —                 |
| 4  | 34   | soil_moistureAn_1| ANALOG_INPUT  | Влажность почвы (аналог)               | AO → GPIO34, питание 3.3V AMS1117, GND общая                     | —                 |
| 5  | 23   | soil_moistureDig_1 | DIGITAL_INPUT | Влажность почвы (цифровой порог)       | DO → GPIO23, питание 3.3V AMS1117, GND общая                     | —                 |
| 6  | 19   | LCD 16x2 I²C     | I²C           | Жидкокристаллический дисплей            | SDA → GPIO21, SCL → GPIO22, питание 5V от MT3608, GND общая      | 0x27              |
| 7  | 18   | ULTRASONIC_TRIG_1 | DIGITAL_OUTPUT | УЗ датчик уровня (Trig)               | OUTPUT, 3.3V, 1 GPIO на Trig                                     | —                 |
| 8  | 25   | ULTRASONIC_ECHO_1 | DIGITAL_INPUT  | УЗ датчик уровня (Echo)               | INPUT, 5V → 3.3V делитель, 1 GPIO на Echo                        | —                 |
| 9  | VIN  | ESP32_POWER       | POWER          | Питание ESP32 DevKit V1                | VIN подключен к OUT+ MT3608, GND к OUT− MT3608                   | —                 |

---

## 4️⃣ Масштабируемость и новые устройства

- Любой новый датчик / ESP32 модуль:
  1. Создаётся папка в `esp32/` или `backend/`.
  2. Добавляется запись в таблицу подключения.
  3. Все I²C устройства должны иметь уникальный адрес.
- Пользователь должен иметь возможность через веб-интерфейс добавлять новые устройства **без изменения кода вручную**.

---

## 5️⃣ Docker и Backend

- **Docker**:
  - Mosquitto → брокер MQTT для передачи данных от ESP32.
  - PostgreSQL → основная база данных.
- **Backend (Python)**:
  - Считывает данные с Raspberry Pi и ESP32.
  - Обрабатывает сигналы и пишет в БД.
  - Предоставляет API для веб-интерфейса.
- **Web / API (HTML + CSS + JS)**:
  - Отображение данных пользователю.
  - Добавление новых датчиков и устройств.
  - Взаимодействие с Backend через REST или WebSocket.

---

## 6️⃣ Пример Python-кода для Raspberry Pi

```python
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # PUMP_1
GPIO.setup(26, GPIO.OUT)  # INLET_VALVE_1

client = mqtt.Client("rasp_pi")
client.connect("localhost", 1883, 60)

def read_sensors():
    # TODO: добавить код для чтения датчиков (DS18B20, ADC, etc.)
    return {"PH": 7.0, "TDS": 300}

def main_loop():
    try:
        while True:
            data = read_sensors()
            client.publish("hydrofarm/sensors", str(data))
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main_loop()

7️⃣ Контракт для разработчиков

Все файлы сохраняются в соответствующих папках.

Любой новый функционал согласуется с командой.

Ветки и Pull Requests используются для согласования изменений.

Таблицы подключения датчиков всегда актуальны.

Новый модуль I²C или аналоговый датчик:

Проверяется на уникальный адрес.

Документируется в docs/schematics/ и в developer_contract.md.

История изменений хранится через GitHub.

8️⃣ Примеры JSON/YAML конфигураций
ESP32
{
  "device_id": "esp32_module_01",
  "sensors": [
    {"type": "CO2/VOC_1", "pin": "I2C", "i2c_address": "0x5A"},
    {"type": "illumination_1", "pin": "I2C", "i2c_address": "0x23"}
  ]
}

Raspberry Pi
{
  "device_id": "raspberry_pi_01",
  "relays": [
    {"name": "PUMP_1", "gpio": 17, "type": "OUTPUT", "active_low": true},
    {"name": "INLET_VALVE_1", "gpio": 26, "type": "OUTPUT", "active_low": true}
  ],
  "analog_sensors": [
    {"name": "PH_SENSOR_1", "adc_channel": "A0", "i2c_address": "0x48"},
    {"name": "TDS_SENSOR_1", "adc_channel": "A1", "i2c_address": "0x49"}
  ],
  "digital_sensors": [
    {"name": "ULTRASONIC_ECHO_1", "gpio": 25},
    {"name": "WATER_TEMP_1", "gpio": 4}
  ]
}

9️⃣ Шаблон веб-интерфейса (для будущей масштабируемости)

Через браузер пользователь сможет:

Добавлять новые ESP32 и датчики.

Вводить параметры подключения (GPIO, I²C, тип датчика).

Конфигурация автоматически обновляется в JSON/YAML.

Все новые устройства сохраняются в esp32/ и таблицах подключения.
