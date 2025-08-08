# app/main.py

from fastapi import FastAPI
from app.endpoints import router as endpoints_router
from app.models import usuarios, roles
from app.database.database import Base, engine, SessionLocal
from app.utils.init_data import insertar_datos_prueba

app = FastAPI(
    title="API - Agro IoT",
    description="Backend del sistema web para gestión de tambos y dispositivos IoT.",
    version="1.0.0"
)

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

# Insertar datos de prueba
with SessionLocal() as db:
    insertar_datos_prueba(db)

# Incluye rutas
app.include_router(endpoints_router)

