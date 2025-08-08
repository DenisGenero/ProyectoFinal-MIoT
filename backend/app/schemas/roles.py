from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str
    es_admin: bool

class RolCreate(RolBase):
    pass

class RolRead(RolBase):
    id: int

    class Config:
        from_attributes = True
