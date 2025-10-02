from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.schemas.token import Token
from app.crud import usuarios as crud_usuarios

router = APIRouter()

@router.post("/auth/register", response_model=UsuarioRead)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud_usuarios.create_usuario(db, usuario)

@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud_usuarios.login_usuario(db, email=form_data.username, password=form_data.password)