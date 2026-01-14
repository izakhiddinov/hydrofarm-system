from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from . import models, database # Убедись, что database.py настроен на SQLAlchemy
from .mqtt_client import start_mqtt # Твой MQTT клиент

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HydroFarm Smart OS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ДЛЯ ТАЛГАТА (Настройки и мониторинг) ---

@app.get("/api/devices")
def get_devices(db: Session = Depends(get_db)):
    return db.query(models.DeviceConfig).all()

@app.post("/api/devices/setup")
def setup_device(config: dict, db: Session = Depends(get_db)):
    dev_id = config.get("id")
    db_device = db.query(models.DeviceConfig).filter(models.DeviceConfig.id == dev_id).first()
    if db_device:
        for key, value in config.items():
            setattr(db_device, key, value)
    else:
        db.add(models.DeviceConfig(**config))
    db.commit()
    return {"status": "success"}

@app.get("/api/data")
def get_sensor_history(db: Session = Depends(get_db)):
    return db.query(models.SensorData).order_by(models.SensorData.created_at.desc()).limit(50).all()

# --- API ДЛЯ УПРАВЛЕНИЯ (Команды) ---

@app.post("/api/command")
def send_command(device_id: str, command: str, db: Session = Depends(get_db)):
    new_cmd = models.DeviceCommand(device_id=device_id, command=command)
    db.add(new_cmd)
    db.commit()
    return {"status": "pending"}

@app.get("/api/agent/get_commands")
def get_agent_commands(device_id: str, db: Session = Depends(get_db)):
    cmds = db.query(models.DeviceCommand).filter(
        models.DeviceCommand.device_id == device_id, 
        models.DeviceCommand.status == "pending"
    ).all()
    for cmd in cmds:
        cmd.status = "sent"
    db.commit()
    return cmds

if __name__ == "__main__":
    # Запуск MQTT в отдельном потоке можно оставить в mqtt_client
    uvicorn.run(app, host="0.0.0.0", port=8000)