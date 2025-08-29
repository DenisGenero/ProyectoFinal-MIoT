from pydantic import BaseModel
from typing import Optional

class ComederoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ubicacion: str

class ComederoCreate(ComederoBase):
    id_tambo: int

class ComederoRead(ComederoBase):
    id: int
    id_tambo: int

    class Config:
        from_attributes = True

class UpdateComedero(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None

    class Config:
        extra= "ignore"
