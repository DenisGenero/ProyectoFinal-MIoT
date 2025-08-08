from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
from app.database.database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    id_comedero = Column(Integer, ForeignKey("comederos.id"))
    nombre = Column(String(100), nullable=False)
    usuario_local = Column(String(100), nullable=False)
    direccion_local = Column(String(100), nullable=False)
    puerto_ssh = Column(Integer, nullable=False)
    usuario_servidor = Column(String(100), nullable=False)
    direccion_servidor = Column(String(100), nullable=False)
    puerto_servidor = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    intervalo = Column(Time, nullable=False)
    estado = Column(Boolean, default=True)

    comedero = relationship("Comedero", back_populates="dispositivos")
    imagenes = relationship("Imagen", back_populates="dispositivo")
