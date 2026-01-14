import os, time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://hydrofarm_user:hydrofarm_pass@hydrofarm-postgres/hydrofarm"

engine = create_engine(DATABASE_URL)

def wait_for_db(engine):
    for i in range(10):
        try:
            connection = engine.connect()
            connection.close()
            print("✅ Database is ready!")
            return
        except OperationalError:
            print(f"⌛ Waiting for database... {i}/10")
            time.sleep(2)
    exit(1)

wait_for_db(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()