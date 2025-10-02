from sqlalchemy.orm import Session
from datetime import datetime
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.core import security
from fastapi import HTTPException
import re
from app import config

def create_usuario(db: Session, usuario: UsuarioCreate):
    if not usuario.nombres:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, usuario.email):
        raise HTTPException(status_code=400, detail="Email inválido")

    if len(usuario.password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")

    usuario.password = security.get_password_hash(usuario.password)
    nuevo_usuario = Usuario(**usuario.model_dump())
    mail_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if mail_existente:
        raise HTTPException(status_code=400, detail="El mail ya está en uso")
    
    try:
        nuevo_usuario.estado = True
        nuevo_usuario.es_superadmin = False
        nuevo_usuario.fecha_alta = datetime.now(config.UY_TZ)
        nuevo_usuario.ultimo_acceso = datetime.now(config.UY_TZ)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")
    
    return nuevo_usuario


def login_usuario(db: Session, email: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not security.verify_password(password, usuario.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    access_token = security.create_access_token(data={"sub": str(usuario.id)})
    usuario.ultimo_acceso =  datetime.now(config.UY_TZ)
    db.commit()
    db.refresh(usuario)
    return {"access_token": access_token, "token_type": "bearer", "user": usuario}


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

def get_usuario_por_mail(db: Session, email: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
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
        if key == "password":
            value = security.get_password_hash(value)
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