from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mqtt_client import start_mqtt
from db import get_connection, init_db
import uvicorn
import threading

app = FastAPI(title="HydroFarm Smart Platform")

# Разрешаем Талгату подключаться к API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. ПОЛУЧЕНИЕ ДАННЫХ (Для графиков Талгата)
@app.get("/data")
def get_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT device_id, sensor_name, value, created_at FROM sensor_data ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"device": r[0], "sensor": r[1], "value": float(r[2]), "time": str(r[3])} for r in rows]
    except Exception as e:
        return {"error": str(e)}

# 2. СПИСОК УСТРОЙСТВ (Чтобы знать, кто в сети)
@app.get("/devices")
def get_devices():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT device_id, device_name, is_active FROM devices")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": r[0], "name": r[1], "active": r[2]} for r in rows]
    except Exception as e:
        return {"error": str(e)}

# 3. ОТПРАВКА КОМАНДЫ (Талгат нажимает кнопку в браузере)
@app.post("/command")
def send_command(device_id: str, command: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO device_commands (device_id, command, status) VALUES (%s, %s, %s)",
            (device_id, command, "pending")
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": f"Команда {command} записана"}
    except Exception as e:
        return {"error": str(e)}

# 4. ВЫДАЧА КОМАНДЫ (Raspberry Pi спрашивает: "Что мне сделать?")
@app.get("/get_commands")
def get_commands(device_id: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Берем самую старую невыполненную команду
        cur.execute(
            "SELECT id, command FROM device_commands WHERE device_id = %s AND status = 'pending' ORDER BY created_at ASC LIMIT 1",
            (device_id,)
        )
        row = cur.fetchone()
        if row:
            cmd_id, cmd_text = row
            # Помечаем, что команда ушла на устройство
            cur.execute("UPDATE device_commands SET status = 'sent' WHERE id = %s", (cmd_id,))
            conn.commit()
            cur.close()
            conn.close()
            return {"command_id": cmd_id, "command": cmd_text}
        
        cur.close()
        conn.close()
        return {"command": None}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🚀 HydroFarm Smart Platform starting...", flush=True)
    init_db() # Проверяем/создаем все таблицы
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    print("📡 API available at http://localhost:8000", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()