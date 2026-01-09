import time
from mqtt_client import start_mqtt

def main():
    mqtt_client = start_mqtt()
    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        print("Backend stopped")

if __name__ == "__main__":
    main()
