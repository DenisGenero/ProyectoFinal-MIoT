from pydantic import BaseModel

# ---- Rol ----
class RolRead(BaseModel):
    id: int
    nombre: str
    es_admin: bool

    class Config:
        from_attributes = True


# ---- Tambo ----
class TamboRead(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    ubicacion: str
    estado: bool

    class Config:
        from_attributes = True


# ---- UsuarioTamboRol ----
class UsuarioTamboRolBase(BaseModel):
    id_usuario: int
    id_tambo: int
    id_rol: int
    estado: bool = True


class UsuarioTamboRolCreate(UsuarioTamboRolBase):
    pass


class UsuarioTamboRolRead(BaseModel):
    tambo: TamboRead
    rol: RolRead

    class Config:
        from_attributes = True
