from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Tambo(Base):
    __tablename__ = "tambos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    ubicacion = Column(String(255), nullable=False)
    estado = Column(Boolean, default=True)

    usuarios_tambos_roles = relationship("UsuarioTamboRol", back_populates="tambo")
    comederos = relationship("Comedero", back_populates="tambo", cascade="all, delete-orphan")