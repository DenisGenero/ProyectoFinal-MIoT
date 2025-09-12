from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Comedero(Base):
    __tablename__ = "comederos"

    id = Column(Integer, primary_key=True, index=True)
    id_tambo = Column(Integer, ForeignKey("tambos.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    ubicacion = Column(String(255), nullable=True)
    estado = Column(Boolean, default=True, nullable=False)

    tambo = relationship("Tambo", back_populates="comederos")
    dispositivos = relationship("Dispositivo", back_populates="comedero", cascade="all, delete")
