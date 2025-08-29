from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from fastapi import HTTPException

UY_TZ = ZoneInfo("America/Montevideo")

def create_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario(**usuario.model_dump())
    mail_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if mail_existente:
        raise HTTPException(status_code=400, detail="El mail ya está en uso")
    
    nuevo_usuario.estado = True
    nuevo_usuario.fecha_alta = datetime.now(UY_TZ)
    nuevo_usuario.ultimo_acceso = datetime.now(UY_TZ)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    usuarios = db.query(Usuario).filter(Usuario.estado == True).offset(skip).limit(limit).all()
    if not usuarios:
        raise HTTPException(status_code=404, detail="Usuarios no encontrados")
    return usuarios

def get_usuario_por_id(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=404, detail="Usuario no inactivo")
    
    return usuario

def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    campos_permitidos = {"nombres", "apellidos", "email", "password"}
    update_data = usuario_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if key not in campos_permitidos:
            continue
        if len(value.strip()) == 0:
            continue
        # Validación email único
        if key == "email":
            email_existente = db.query(Usuario).filter(
                Usuario.email == value,
                Usuario.id != usuario_id
            ).first()
            if email_existente:
                raise HTTPException(status_code=400, detail="El email ya está en uso")
        setattr(usuario, key, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

def deactivate_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=400, detail="Usuario ya desactivado")
    
    usuario.estado = False
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} desactivado"}

def activate_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == True:
        raise HTTPException(status_code=400, detail="Usuario ya activado")
    
    usuario.estado = True
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} recuperado"}

def delete_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} eliminado"}