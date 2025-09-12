from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
from app.database.database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    id_comedero = Column(Integer, ForeignKey("comederos.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    usuario_local = Column(String(100), nullable=True)
    direccion_local = Column(String(100), nullable=True)
    puerto_ssh = Column(Integer, nullable=True)
    usuario_servidor = Column(String(100), nullable=True)
    direccion_servidor = Column(String(100), nullable=True)
    puerto_servidor = Column(Integer, nullable=True)
    mac_address = Column(String(17), unique=True, nullable=True)
    hora_inicio = Column(Time, nullable=True)
    hora_fin = Column(Time, nullable=True)
    intervalo = Column(Integer, nullable=True)
    estado = Column(Boolean, default=False, nullable=False)

    comedero = relationship("Comedero", back_populates="dispositivos")
    imagenes = relationship("Imagen", back_populates="dispositivo")
