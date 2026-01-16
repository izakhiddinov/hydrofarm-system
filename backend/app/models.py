import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from db import Base

class ComponentLibrary(Base):
    """Справочник доступного оборудования (наш склад)"""
    __tablename__ = "component_library"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)     # Pump, Valve, Sensor, etc.
    direction = Column(String)    # IN (вход) / OUT (выход)
    model_name = Column(String)   # ESPA Aspri 15
    voltage = Column(String)      # 220V, 12V
    interface = Column(String)    # GPIO, Modbus, Analog
    schema_svg = Column(String)   # Здесь будет название файла схемы

class DeviceConfig(Base):
    """Таблица настроенных устройств на ферме"""
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    device_type = Column(String)
    connection_type = Column(String) # GPIO / Modbus
    pin_number = Column(Integer)     # Номер пина
    model_selected = Column(String)  # Какую модель из библиотеки выбрали
    status = Column(String, default="offline")
    # Добавляем поле для хранения дополнительных настроек
    extra_data = Column(JSON, nullable=True) 

class DeviceCommand(Base):
    __tablename__ = "device_commands"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    command = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)