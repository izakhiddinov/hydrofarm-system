CREATE TABLE IF NOT EXISTS sensor_types (
    id SERIAL PRIMARY KEY,
    type_name TEXT UNIQUE,
    unit TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    device_name TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    device_id TEXT REFERENCES devices(device_id),
    sensor_name TEXT,
    value NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Наполняем базу базовыми типами
INSERT INTO sensor_types (type_name, unit, description) VALUES 
('temperature', '°C', 'Температура'),
('humidity', '%', 'Влажность'),
('water_level', 'cm', 'Уровень воды'),
('ph', 'pH', 'Кислотность');

-- Регистрируем твою Raspberry Pi
INSERT INTO devices (device_id, device_name, is_active) 
VALUES ('rpi5_main', 'Raspberry Pi 5 Central', TRUE)
ON CONFLICT (device_id) DO NOTHING;