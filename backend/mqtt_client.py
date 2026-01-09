import paho.mqtt.client as mqtt
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT

def on_connect(client, userdata, flags, rc):
    print(f"MQTT connected with code {rc}")
    client.subscribe("hydrofarm/#")

def on_message(client, userdata, msg):
    print(f"MQTT message: {msg.topic} -> {msg.payload.decode()}")

def start_mqtt():
    client = mqtt.Client("hydrofarm_backend")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    return client
