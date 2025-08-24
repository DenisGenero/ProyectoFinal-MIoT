from fastapi import FastAPI
from app.endpoints import router as endpoints_router
from app.database.database import Base, engine, SessionLocal
from app.utils.init_data import insertar_datos_prueba
from app.utils.init_db import crear_base_datos

app = FastAPI(
    title="API - Agro IoT",
    description="Backend del sistema web para gestión de tambos y dispositivos IoT.",
    version="1.0.0"
)

# Crear la base de datos si no existe
crear_base_datos()

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Insertar datos de prueba
with SessionLocal() as db:
    insertar_datos_prueba(db)

# Incluir rutas
app.include_router(endpoints_router)

