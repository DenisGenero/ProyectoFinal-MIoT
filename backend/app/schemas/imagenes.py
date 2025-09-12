from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImagenBase(BaseModel):
    path_imagen: str
    fecha: datetime

class ImagenCreate(ImagenBase):
    pass

class ImagenRead(ImagenBase):
    id: int
    id_dispositivo: int

    class Config:
        from_attributes = True

class UpdateImagen(BaseModel):
    path_imagen: Optional[str] = None

    class Config:
        extra= "ignore"
