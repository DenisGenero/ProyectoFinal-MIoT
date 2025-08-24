from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from zoneinfo import ZoneInfo
from typing import Optional

UY_TZ = ZoneInfo("America/Montevideo")

class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    estado: bool = True

class UsuarioCreate(UsuarioBase):
    password: str
    fecha_alta: datetime = Field(default_factory=lambda: datetime.now(UY_TZ))
    ultimo_acceso: datetime = Field(default_factory=lambda: datetime.now(UY_TZ))


class UsuarioRead(UsuarioBase):
    id: int
    ultimo_acceso: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class config:
        extra = "ignore"  # "ignore" ignora los demás campos;  "forbid" --> arroja error
