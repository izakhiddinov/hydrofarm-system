import time
import requests
import os

# Настройки (PYTHONUNBUFFERED в Docker позволит видеть эти логи сразу)
API_URL = os.getenv("API_URL", "http://hydrofarm-backend:8000")
DEVICE_ID = "rpi5_main"

# ПОЛНАЯ ТАБЛИЦА ПОДКЛЮЧЕНИЙ (согласно твоему ТЗ)
PIN_MAP = {
    "PUMP_1": 17,
    "PUMP_2": 27,
    "PUMP_3": 5,
    "PUMP_4": 6,
    "PUMP_5": 13,
    "PUMP_6": 19,
    "LIGHT_1": 22,
    "FAN_1": 23,
    "INLET_VALVE_1": 26,
    "FILL_VALVE_2": 24
}

def execute_command(command_text):
    # Ищем, какое устройство упоминается в тексте команды
    for dev_name, pin in PIN_MAP.items():
        if dev_name in command_text:
            state = "ON" if "ON" in command_text else "OFF"
            # Active LOW: ON = 0V (LOW), OFF = 3.3V (HIGH)
            logic_level = "LOW (0V)" if state == "ON" else "HIGH (3.3V)"
            
            print(f"---")
            print(f"📥 ПОЛУЧЕНА КОМАНДА: {command_text}")
            print(f"⚙️ ПИН {pin}: {dev_name} переведен в {state} [{logic_level}]")
            print(f"---")
            return
    print(f"⚠️ Внимание: Устройство в команде '{command_text}' не найдено в PIN_MAP")

def main():
    print(f"🚀 Агент {DEVICE_ID} запущен и готов к работе.")
    print(f"📋 Загружено устройств: {len(PIN_MAP)}")
    
    while True:
        try:
            # Опрашиваем бэкенд на наличие новых команд
            response = requests.get(f"{API_URL}/get_commands", params={"device_id": DEVICE_ID}, timeout=5)
            if response.status_code == 200:
                commands = response.json()
                for cmd in commands:
                    execute_command(cmd["command"])
            
        except Exception as e:
            print(f"❌ Ошибка связи с API: {e}")
        
        time.sleep(2) # Интервал опроса

if __name__ == "__main__":
    main()