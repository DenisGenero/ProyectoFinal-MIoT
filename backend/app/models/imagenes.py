from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    id_dispositivo = Column(Integer, ForeignKey("dispositivos.id"))
    path_imagen = Column(String(100), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    dispositivo = relationship("Dispositivo", back_populates="imagenes")
