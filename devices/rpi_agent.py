import time, requests, os

API_URL = os.getenv("API_URL", "http://hydrofarm-backend:8000")
DEVICE_ID = "rpi5_main"

class HydroAgent:
    def __init__(self):
        self.devices = {}

    def sync_hardware_map(self):
        try:
            r = requests.get(f"{API_URL}/api/devices")
            if r.status_code == 200:
                self.devices = {d['id']: d for d in r.json()}
        except:
            print("❌ Ошибка синхронизации конфига")

    def run_command(self, cmd_text, device_id):
        config = self.devices.get(device_id)
        if not config: return
        
        state = "ON" if "ON" in cmd_text else "OFF"
        
        if config['connection_type'] == "relay":
            print(f"🔌 GPIO {config['pin_number']} -> {state} (RELAY)")
            # Здесь физический вызов RPi.GPIO
        elif config['connection_type'] == "modbus":
            print(f"📟 MODBUS {config['modbus_address']} -> {state} (INVERTER)")

    def start(self):
        while True:
            self.sync_hardware_map()
            try:
                r = requests.get(f"{API_URL}/api/agent/get_commands", params={"device_id": DEVICE_ID})
                if r.status_code == 200:
                    for c in r.json():
                        self.run_command(c['command'], c['device_id'])
            except: pass
            time.sleep(2)

if __name__ == "__main__":
    HydroAgent().start()