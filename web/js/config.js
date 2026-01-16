// Карта специализации пинов на основе ваших PDF-схем [cite: 32, 63, 132, 175]
export const RPI5_PINOUT = {
    1: { type: 'system', label: '3.3V' }, 2: { type: 'system', label: '5V' },
    3: { type: 'special', label: 'SDA1', msg: 'I2C: Для ADS1115 (pH/TDS)' },
    4: { type: 'system', label: '5V' },
    5: { type: 'special', label: 'SCL1', msg: 'I2C: Для ADS1115 (pH/TDS)' },
    6: { type: 'system', label: 'GND' },
    8: { type: 'special', label: 'TXD0', msg: 'UART: Для Modbus/Инверторов' },
    9: { type: 'system', label: 'GND' },
    10: { type: 'special', label: 'RXD0', msg: 'UART: Для Modbus/Инверторов' },
    14: { type: 'system', label: 'GND' }, 20: { type: 'system', label: 'GND' },
    25: { type: 'system', label: 'GND' }, 30: { type: 'system', label: 'GND' },
    34: { type: 'system', label: 'GND' }, 39: { type: 'system', label: 'GND' }
};

// Рекомендации из "Заметок программиста" для быстрой подсветки [cite: 32, 63, 132, 175]
export const RECOMMENDATIONS = {
    21: "FLOW_SENSOR_1",
    26: "INLET_VALVE_1",
    17: "PUMP_1",
    27: "PUMP_2",
    4:  "WATER_TEMP_1",
    18: "US_TRIG",
    25: "US_ECHO"
};