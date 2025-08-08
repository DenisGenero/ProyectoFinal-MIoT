from pydantic import BaseModel
from datetime import datetime

class ImagenBase(BaseModel):
    id_dispositivo: int
    path_imagen: str

class ImagenCreate(ImagenBase):
    pass

class ImagenRead(ImagenBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
