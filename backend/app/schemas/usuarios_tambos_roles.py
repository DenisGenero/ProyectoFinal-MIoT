from pydantic import BaseModel

class UsuarioTamboRolBase(BaseModel):
    id_usuario: int
    id_tambo: int
    id_rol: int
    estado: bool = True

class UsuarioTamboRolCreate(UsuarioTamboRolBase):
    pass

class UsuarioTamboRolRead(UsuarioTamboRolBase):
    class Config:
        from_attributes = True
