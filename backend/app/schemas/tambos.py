from pydantic import BaseModel
from typing import Optional

class TamboBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ubicacion: str
    estado: bool = True

class TamboCreate(TamboBase):
    pass

class TamboRead(TamboBase):
    id: int

    class Config:
        from_attributes = True

class TamboUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None

    class Config:
        extra = "ignore"
