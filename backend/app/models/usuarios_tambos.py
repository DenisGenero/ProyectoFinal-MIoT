from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database.database import Base

class UsuarioTambo(Base):
    __tablename__ = "usuarios_tambos"

    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    id_tambo = Column(Integer, ForeignKey("tambos.id"), primary_key=True)
