import psycopg2
from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

# ВОТ ЭТОЙ ФУНКЦИИ У ТЕБЯ СЕЙЧАС НЕ ХВАТАЕТ:
def save_sensor_data(device_id, sensor_name, value):
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
        print(f"✅ Данные сохранены: {sensor_name} = {value}")
    except Exception as e:
        print(f"❌ Ошибка записи в БД: {e}")