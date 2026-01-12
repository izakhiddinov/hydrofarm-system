# backend/main.py
from fastapi import FastAPI
from mqtt_client import start_mqtt
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("HydroFarm backend starting...")
    # Запускаем MQTT в фоне
    asyncio.create_task(start_mqtt())

@app.get("/status")
async def status():
    return {"status": "ok"}
