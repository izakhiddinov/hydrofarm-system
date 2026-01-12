from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mqtt_client import start_mqtt
from db import get_connection, init_db
import uvicorn
import threading

app = FastAPI(title="HydroFarm Smart Platform")

# Настройка CORS, чтобы Талгат мог подключаться со своего компьютера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def main():
    print("🚀 HydroFarm Smart Platform starting...", flush=True)
    
    # Сначала проверяем базу и создаем таблицы
    init_db()

    # Затем запускаем MQTT клиент в отдельном потоке
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    
    print("📡 API available at http://localhost:8000", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()