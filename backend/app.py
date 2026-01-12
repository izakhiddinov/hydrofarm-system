from fastapi import FastAPI
from mqtt_client import start_mqtt
from db import get_connection
import uvicorn
import threading

# 1. Создаем само приложение ("дверь", в которую будет стучаться фронтенд)
app = FastAPI(title="HydroFarm API")

# 2. Создаем маршрут /data. Когда напарник перейдет по ссылке, сработает этот код
@app.get("/data")
def get_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Достаем последние 50 записей из базы
        cur.execute("SELECT device_id, sensor_name, value, created_at FROM sensor_data ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Превращаем данные из базы в понятный для фронтенда список
        return [{"device": r[0], "sensor": r[1], "value": float(r[2]), "time": str(r[3])} for r in rows]
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🌱 HydroFarm API Server starting...", flush=True)
    
    # 3. Запускаем MQTT в фоновом потоке (чтобы он продолжал ловить данные и не мешал серверу)
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    
    # 4. Запускаем сам веб-сервер на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()