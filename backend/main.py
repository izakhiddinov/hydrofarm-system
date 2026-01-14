from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import db
from app import models

# Создаем таблицы в базе
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="HydroFarm PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/devices")
def get_devices(database: Session = Depends(db.get_db)):
    return database.query(models.DeviceConfig).all()

@app.post("/api/devices/setup")
def setup_device(config: dict, database: Session = Depends(db.get_db)):
    dev_id = config.get("id")
    db_device = database.query(models.DeviceConfig).filter(models.DeviceConfig.id == dev_id).first()
    if db_device:
        for key, value in config.items(): setattr(db_device, key, value)
    else:
        database.add(models.DeviceConfig(**config))
    database.commit()
    return {"status": "success"}

@app.get("/status")
def status():
    return {"status": "online"}