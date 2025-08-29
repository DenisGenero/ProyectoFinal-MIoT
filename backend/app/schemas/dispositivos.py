from pydantic import BaseModel
from datetime import time
from typing import Optional

class DispositivoBase(BaseModel):
    id_comedero: int
    nombre: str
    usuario_local: str
    direccion_local: str
    puerto_ssh: int
    usuario_servidor: str
    direccion_servidor: str
    puerto_servidor: int
    hora_inicio: time
    hora_fin: time
    intervalo: time

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoRead(DispositivoBase):
    id: int

    class Config:
        from_attributes = True

class UpdateDispositivo(BaseModel):
    nombre: Optional[str] = None
    usuario_local: Optional[str] = None
    direccion_local: Optional[str] = None
    puerto_ssh: Optional[int] = None
    usuario_servidor: Optional[str] = None
    direccion_servidor: Optional[str] = None
    puerto_servidor: Optional[int] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    intervalo: Optional[time] = None

    class Config:
        extra= "ignore"