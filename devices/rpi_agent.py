import time
import requests

# --- НАСТРОЙКИ ---
API_URL = "http://hydrofarm-backend:8000"
DEVICE_ID = "rpi5_main"

# ПИНЫ ИЗ ТВОЕЙ ТАБЛИЦЫ (BCM нумерация)
PUMPS = {
    "PUMP_1": 17,  # Основной насос
    "PUMP_2": 27,  # Резервный насос
    "PUMP_3": 5,   # Дозирующий 1
    "PUMP_4": 6,   # Дозирующий 2
    "PUMP_5": 13,  # Дозирующий 3
    "PUMP_6": 19,  # Дозирующий 4
}
VALVES = {
    "INLET_VALVE": 26, # Клапан подачи
    "FILL_VALVE": 24   # Клапан долива
}
OTHERS = {
    "LIGHT": 22, # Свет
    "FAN": 23    # Вентиляторы
}

print(f"🚀 Агент {DEVICE_ID} запущен по твоей схеме подлючений.")

def execute_action(cmd):
    """Логика сопоставления команд с пинами из таблицы"""
    
    # ПРИМЕР: Команда "PUMP_1_ON"
    if cmd.endswith("_ON") or cmd.endswith("_OFF"):
        action = "ON" if cmd.endswith("_ON") else "OFF"
        base_cmd = cmd.replace("_ON", "").replace("_OFF", "")
        
        # Проверяем, есть ли такой прибор в наших списках
        pin = None
        if base_cmd in PUMPS: pin = PUMPS[base_cmd]
        elif base_cmd in VALVES: pin = VALVES[base_cmd]
        elif base_cmd in OTHERS: pin = OTHERS[base_cmd]

        if pin:
            state = "ПОДАЮ ТОК (LOW)" if action == "ON" else "ВЫКЛЮЧАЮ (HIGH)"
            # Внимание: в твоей таблице указано ACTIVE LOW (реле включается от 0)
            print(f"⚙️ Пин {pin}: {base_cmd} -> {action} [{state}]")
        else:
            print(f"❓ Неизвестное устройство в команде: {cmd}")

def work_loop():
    while True:
        try:
            response = requests.get(f"{API_URL}/get_commands", params={"device_id": DEVICE_ID})
            if response.status_code == 200:
                data = response.json()
                if data.get("command"):
                    execute_action(data["command"])
            
        except Exception as e:
            print(f"🔌 Ошибка связи: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    work_loop()