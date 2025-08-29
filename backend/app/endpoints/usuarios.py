from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.usuarios import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.crud import usuarios as crud_usuarios

router = APIRouter()

@router.post("/usuarios/", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud_usuarios.create_usuario(db, usuario)

@router.get("/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_usuarios.get_usuarios(db, skip, limit)

@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.get_usuario_por_id(db, usuario_id)

@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)):
    return crud_usuarios.update_usuario(db, usuario_id, usuario_data)

@router.put("/usuarios/{usuario_id}/desactivar")
def desactivar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.deactivate_usuario(db, usuario_id)

@router.put("/usuarios/{usuario_id}/recuperar")
def activar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.activate_usuario(db, usuario_id)

@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.delete_usuario(db, usuario_id)
