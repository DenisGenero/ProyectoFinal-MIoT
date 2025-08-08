# app/endpoints/usuarios.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.crud import usuarios as crud_usuarios

router = APIRouter()

@router.post("/usuarios/", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud_usuarios.create_usuario(db, usuario)

@router.get("/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud_usuarios.get_usuarios(db)

@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_usuarios.get_usuario_por_id(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.delete_usuario(db, usuario_id)