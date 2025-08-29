from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int
    fecha_alta: datetime
    ultimo_acceso: datetime

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        extra = "ignore"  # "ignore" ignora los demás campos;  "forbid" --> arroja error
