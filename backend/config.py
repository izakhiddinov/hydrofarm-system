import os

# MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_SENSORS = "hydrofarm/sensors/#"
MQTT_TOPIC_COMMANDS = "hydrofarm/commands/#"

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hydrofarm")
POSTGRES_USER = os.getenv("POSTGRES_USER", "hydrofarm_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "hydrofarm_pass")

# System
DEBUG = True
