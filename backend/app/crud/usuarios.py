from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate
from fastapi import HTTPException

def create_usuario(db: Session, usuario: UsuarioCreate):
    # nuevo_usuario = Usuario(**usuario.dict())
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_por_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def delete_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario con ID {usuario_id} eliminado"}