import psycopg2
import os
import time

def get_connection():
    """Создает подключение к PostgreSQL с несколькими попытками"""
    for i in range(5):
        try:
            return psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                database=os.getenv("POSTGRES_DB", "hydrofarm"),
                user=os.getenv("POSTGRES_USER", "hydrofarm_user"),
                password=os.getenv("POSTGRES_PASSWORD", "hydrofarm_pass")
            )
        except Exception as e:
            print(f"⌛ Ожидание базы данных (попытка {i+1})... {e}")
            time.sleep(2)
    raise Exception("Не удалось подключиться к PostgreSQL")

def init_db():
    """Автоматическое создание всех таблиц при старте бэкенда"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Создаем структуру таблиц
        cur.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_name TEXT,
                is_active BOOLEAN DEFAULT FALSE,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                device_id TEXT,
                sensor_name TEXT,
                value NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS device_commands (
                id SERIAL PRIMARY KEY,
                device_id TEXT,
                command TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Регистрируем базовое устройство
        cur.execute("""
            INSERT INTO devices (device_id, device_name, is_active) 
            VALUES ('rpi5_main', 'Raspberry Pi 5 Central', TRUE)
            ON CONFLICT (device_id) DO NOTHING;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ База данных успешно инициализирована (все таблицы на месте).", flush=True)
    except Exception as e:
        print(f"❌ Ошибка инициализации базы: {e}", flush=True)

def save_sensor_data(device_id, sensor_name, value):
    """Сохраняет данные от датчиков в базу (вызывается из mqtt_client.py)"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sensor_data (device_id, sensor_name, value) VALUES (%s, %s, %s)",
            (device_id, sensor_name, value)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка сохранения данных в MQTT: {e}", flush=True)