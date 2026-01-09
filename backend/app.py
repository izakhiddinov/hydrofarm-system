from mqtt_client import start_mqtt
import time

def main():
    print("HydroFarm backend starting...")
    mqtt_client = start_mqtt()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping backend")

if __name__ == "__main__":
    main()
