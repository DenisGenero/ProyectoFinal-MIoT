from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    es_admin = Column(Boolean, nullable=False)
    estado = Column(Boolean, nullable=False, default=True)

    usuarios_tambos_roles = relationship("UsuarioTamboRol", back_populates="rol")