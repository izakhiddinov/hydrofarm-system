import paho.mqtt.client as mqtt
import json
import time
import random
import sys

# Настройки
BROKER = "mosquitto" 
PORT = 1883
TOPIC = "hydrofarm/sensors/esp32_01"

# Новая версия библиотеки требует указания CallbackAPIVersion
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("🚀 Симулятор ESP32 запущен. Шлю данные...", flush=True)

try:
    client.connect(BROKER, PORT)
    while True:
        data = {
            "device_id": "esp32_01",
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 70.0), 2)
        }
        
        client.publish(TOPIC, json.dumps(data))
        print(f"📡 Отправлено: {data}", flush=True) # flush=True заставляет текст сразу лететь в логи
        
        time.sleep(5)
except Exception as e:
    print(f"❌ Ошибка симулятора: {e}", flush=True)