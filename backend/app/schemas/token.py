from pydantic import BaseModel
from app.schemas.usuarios import UsuarioRead

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioRead