from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(50), nullable=False)
    fecha_alta = Column(DateTime)
    ultimo_acceso = Column(DateTime)
    estado = Column(Boolean, nullable=True)

    usuarios_tambos_roles = relationship("UsuarioTamboRol", back_populates="usuario", cascade="all, delete-orphan")