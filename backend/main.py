import json
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Наши внутренние модули
import db
from app import models

# 1. Автоматическое создание таблиц в Postgres (настройки устройств)
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="HydroFarm PRO API")

# Настройка CORS (чтобы фронтенд мог обращаться к бэкенду)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- РАБОТА С КАТАЛОГОМ (ЛОКАЛЬНЫЙ СКЛАД / МАГАЗИН) ---

@app.get("/api/catalog")
def get_catalog(direction: str = None):
    """Читает список доступного оборудования из JSON файла"""
    catalog_path = "backend/data/catalog.json"
    
    # Проверка, существует ли файл, чтобы сервер не упал
    if not os.path.exists(catalog_path):
        return {"error": f"Файл каталога не найден по пути: {catalog_path}"}
    
    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if direction:
            # Фильтруем: IN, OUT или устройства двойного назначения IN_OUT
            return [item for item in data if item["direction"] == direction or item["direction"] == "IN_OUT"]
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения каталога: {str(e)}")


# --- РАБОТА С НАСТРОЕННЫМИ УСТРОЙСТВАМИ (БАЗА POSTGRES) ---

@app.get("/api/devices")
def get_devices(database: Session = Depends(db.get_db)):
    """Возвращает список устройств, которые уже настроены и сохранены в БД"""
    return database.query(models.DeviceConfig).all()

@app.post("/api/devices/setup")
def setup_device(config: dict, database: Session = Depends(db.get_db)):
    """Сохраняет выбор администратора в базу данных"""
    dev_id = config.get("id")
    if not dev_id:
        raise HTTPException(status_code=400, detail="ID устройства не указан")

    db_device = database.query(models.DeviceConfig).filter(models.DeviceConfig.id == dev_id).first()
    
    if db_device:
        # Если такое устройство уже настраивали — обновляем данные
        for key, value in config.items():
            setattr(db_device, key, value)
    else:
        # Если новое — создаем запись
        new_device = models.DeviceConfig(**config)
        database.add(new_device)
    
    database.commit()
    return {"status": "success", "message": f"Устройство {dev_id} успешно настроено"}

@app.get("/status")
def status():
    """Проверка жизнеспособности бэкенда"""
    return {"status": "online", "database": "connected"}