from pydantic import BaseModel
from datetime import time
from typing import Optional

class DispositivoBase(BaseModel):
    nombre: str

class DispositivoCreate(DispositivoBase):
    id_comedero: int

class DispositivoConfig(BaseModel):
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    intervalo: Optional[int] = None

class DispositivoAdmin(BaseModel):
    usuario_local: Optional[str] = None
    direccion_local: Optional[str] = None
    puerto_ssh: Optional[int] = None
    usuario_servidor: Optional[str] = None
    direccion_servidor: Optional[str] = None
    puerto_servidor: Optional[int] = None
    mac_address: Optional[str] = None

class DispositivoConfigRead(DispositivoBase, DispositivoConfig):
    id: int
    id_comedero: int

    class Config:
        from_attributes = True

class DispositivoAdminRead(DispositivoBase, DispositivoAdmin):
    id: int
    id_comedero: int

    class Config:
        from_attributes = True

"""
class DispositivoReadAdmin(DispositivoBase):
    id: int
    id_comedero: int
    config: Optional[DispositivoConfig] = None
    admin_config: Optional[DispositivoAdmin] = None

    class Config:
        from_attributes = True
"""

class UpdateDispositivo(BaseModel):
    nombre: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    intervalo: Optional[int] = None

    class Config:
        extra= "ignore"

class UpdateDispositivoAdmin(DispositivoAdmin):
    usuario_local: Optional[str] = None
    direccion_local: Optional[str] = None
    puerto_ssh: Optional[int] = None
    usuario_servidor: Optional[str] = None
    direccion_servidor: Optional[str] = None
    puerto_servidor: Optional[int] = None
    mac_address: Optional[str] = None