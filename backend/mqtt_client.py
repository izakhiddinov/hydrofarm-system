import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code", rc)
    client.subscribe("hydrofarm/#")

def on_message(client, userdata, msg):
    print(f"MQTT message: {msg.topic} → {msg.payload.decode()}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
    return client
