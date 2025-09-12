from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class UsuarioTamboRol(Base):
    __tablename__ = "usuarios_tambo_roles"

    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_tambo = Column(Integer, ForeignKey("tambos.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=True, nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="usuarios_tambos_roles")
    tambo = relationship("Tambo", back_populates="usuarios_tambos_roles")
    rol = relationship("Rol", back_populates="usuarios_tambos_roles")

