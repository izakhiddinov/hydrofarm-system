from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class DeviceConfig(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True, index=True) # pump_1
    device_type = Column(String, default="pump")    # pump, valve, light
    label = Column(String)                           # Насос основной
    connection_type = Column(String, default="relay") # relay, modbus
    pin_number = Column(Integer, nullable=True)
    modbus_address = Column(Integer, nullable=True)
    has_speed_control = Column(Boolean, default=False)
    backup_device_id = Column(String, nullable=True)
    status = Column(String, default="offline")

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    sensor_name = Column(String)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DeviceCommand(Base):
    __tablename__ = "device_commands"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    command = Column(String)
    status = Column(String, default="pending") # pending, sent, executed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)