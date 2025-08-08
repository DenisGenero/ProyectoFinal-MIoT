from datetime import datetime, UTC
from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    estado: bool
    id_rol: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int
    fecha_alta: datetime = Field(default_factory=lambda: datetime.now(UTC))
    ultimo_acceso: datetime | None = None

    class Config:
        from_attributes = True

