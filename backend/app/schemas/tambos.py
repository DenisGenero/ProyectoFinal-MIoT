from pydantic import BaseModel

class TamboBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    ubicacion: str
    estado: bool

class TamboCreate(TamboBase):
    pass

class TamboRead(TamboBase):
    id: int

    class Config:
        from_attributes = True
