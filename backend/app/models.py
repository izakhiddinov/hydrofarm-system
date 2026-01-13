from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class DeviceConfig(Base):
    """
    Универсальная таблица для ВСЕХ устройств (насосы, клапаны, свет).
    Пользователь может добавлять их по одному, менять пины или переходить на инверторы.
    """
    __tablename__ = "devices"

    # Уникальный ID, например 'pump_main' или 'valve_1'
    id = Column(String, primary_key=True, index=True)
    
    # Что это? 'pump' (насос), 'valve' (клапан), 'fan' (вентилятор), 'light' (свет)
    device_type = Column(String, default="pump")
    
    # Красивое имя для пользователя: 'Главный полив'
    label = Column(String)
    
    # Выбор: 'relay' (GPIO) или 'modbus' (Инвертор)
    connection_type = Column(String, default="relay")
    
    # Номер пина (если реле)
    pin_number = Column(Integer, nullable=True)
    
    # Адрес Modbus (если инвертор)
    modbus_address = Column(Integer, nullable=True)
    
    # Доп. настройки
    has_speed_control = Column(Boolean, default=False) # Есть ли ползунок скорости
    backup_device_id = Column(String, nullable=True)   # ID насоса-дублера
    
    status = Column(String, default="offline")