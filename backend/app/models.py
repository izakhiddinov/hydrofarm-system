import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
# Важно: импортируем Base из db.py, который лежит в папке выше
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Base

class DeviceConfig(Base):
    """Таблица устройств: сюда Мастер Настройки будет записывать новые насосы/клапаны"""
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True) # например: pump_main
    device_type = Column(String, default="pump")    # тип: насос, свет, клапан
    label = Column(String)                           # Имя для сайта (напр. "Полив огурцов")
    connection_type = Column(String, default="relay") # relay (реле) или modbus
    pin_number = Column(Integer, nullable=True)      # номер GPIO на Raspberry
    modbus_address = Column(Integer, nullable=True)  # адрес для инвертора
    status = Column(String, default="offline")

class DeviceCommand(Base):
    """Таблица команд: сюда Талгат шлет сигналы 'Включить/Выключить'"""
    __tablename__ = "device_commands"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    command = Column(String)
    status = Column(String, default="pending") # pending (ждет), sent (отправлено)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)