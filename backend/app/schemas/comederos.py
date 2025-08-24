from pydantic import BaseModel
from typing import Optional

class ComederoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ubicacion: str
    estado: bool

class ComederoCreate(ComederoBase):
    id_tambo: int

class ComederoRead(ComederoBase):
    id: int
    id_tambo: int

    class Config:
        from_attributes = True
