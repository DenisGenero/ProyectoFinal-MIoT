from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    es_admin = Column(Boolean, nullable=False)

