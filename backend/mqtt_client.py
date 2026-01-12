import paho.mqtt.client as mqtt
import json
from config import MQTT_BROKER, MQTT_PORT
from db import save_sensor_data  # Импортируем функцию записи в базу

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ Подключено к MQTT Брокеру с кодом: {rc}")
    # Подписываемся на все датчики в этой ветке
    client.subscribe("hydrofarm/sensors/#")

def on_message(client, userdata, msg):
    try:
        # 1. Декодируем текст из сообщения
        payload_str = msg.payload.decode()
        # 2. Превращаем текст (JSON) в словарь Python
        data = json.loads(payload_str)
        
        device_id = data.get("device_id", "unknown")
        
        # 3. Перебираем все ключи в сообщении (температура, влажность и т.д.)
        for key, value in data.items():
            if key != "device_id":
                # 4. Вызываем функцию сохранения из db.py
                save_sensor_data(device_id, key, value)
                
    except Exception as e:
        print(f"❌ Ошибка при разборе сообщения: {e}")

def start_mqtt():
    # Используем версию API 2 для стабильности
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        return client
    except Exception as e:
        print(f"❌ Не удалось подключиться к MQTT: {e}")
        return None