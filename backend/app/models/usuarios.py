# app/models/usuarios.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.roles import Rol
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
    id_rol = Column(Integer, ForeignKey("roles.id"))
    estado = Column(Boolean, nullable=True)

    rol = relationship("Rol", backref="usuarios")
    tambos = relationship("Tambo", secondary="usuarios_tambos", back_populates="usuarios")