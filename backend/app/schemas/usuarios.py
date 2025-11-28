from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
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
    es_superadmin: bool

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('email', mode='before')
    def handle_empty_email(cls, v):
        # Si el valor es un string vacío, lo convierte a None
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    class Config:
        extra = "ignore"  # "ignore" ignora los demás campos;  "forbid" --> arroja error
