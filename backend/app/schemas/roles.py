from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    es_admin: bool

class RolCreate(RolBase):
    pass

class RolRead(RolBase):
    id: int

    class Config:
        from_attributes = True

class UpdateRol(BaseModel):
    nombre: Optional[str] | None
    es_admin: Optional[bool] | None

    class config:
        extra= "ignore"

