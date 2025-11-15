from fastapi import FastAPI
from app.endpoints import router as endpoints_router
from app.database.database import Base, engine, SessionLocal
from app.utils.init_data import insertar_datos_prueba
from app.utils.init_db import crear_base_datos
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import app.config as config
import os

origins = [
    "http://localhost:5137",
    "http://127.0.0.1:5137",
    "http://164.73.72.30:5137"
]

app = FastAPI(
    title="API - Agro IoT",
    description="Backend del sistema web para gestión de tambos y dispositivos IoT.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path = config.IMAGES_PATH
app.mount("/imagenes", StaticFiles(directory=path, html=True), name="imagenes")

# Crear la base de datos si no existe
crear_base_datos()

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Insertar datos de prueba
with SessionLocal() as db:
    insertar_datos_prueba(db)

# Incluir rutas
app.include_router(endpoints_router)

