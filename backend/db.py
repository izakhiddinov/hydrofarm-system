def init_db():
    """Автоматическое создание таблиц при старте бэкенда"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Создаем таблицы
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

            -- ТАБЛИЦА ДЛЯ КОМАНД (Насосы, свет и т.д.)
            CREATE TABLE IF NOT EXISTS device_commands (
                id SERIAL PRIMARY KEY,
                device_id TEXT,
                command TEXT,      -- 'PUMP_ON', 'PUMP_OFF'
                status TEXT DEFAULT 'pending', 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Регистрация Raspberry
        cur.execute("""
            INSERT INTO devices (device_id, device_name, is_active) 
            VALUES ('rpi5_main', 'Raspberry Pi 5 Central', TRUE)
            ON CONFLICT (device_id) DO NOTHING;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ База данных успешно инициализирована.", flush=True)
    except Exception as e:
        print(f"❌ Ошибка инициализации базы: {e}", flush=True)