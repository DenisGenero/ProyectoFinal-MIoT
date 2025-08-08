# app/schemas/dispositivos.py

from pydantic import BaseModel
from datetime import time

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
    estado: bool

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoRead(DispositivoBase):
    id: int

    class Config:
        orm_mode = True
