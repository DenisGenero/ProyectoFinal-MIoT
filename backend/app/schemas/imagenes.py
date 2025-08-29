from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImagenBase(BaseModel):
    id_dispositivo: int
    path_imagen: str

class ImagenCreate(ImagenBase):
    pass

class ImagenRead(ImagenBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

class UpdateImagen(BaseModel):
    path_imagen: Optional[str] = None
    #fecha: Optinal[datetime] | None

    class Config:
        extra= "ignore"
