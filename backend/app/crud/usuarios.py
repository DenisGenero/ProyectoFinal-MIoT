from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from fastapi import HTTPException

def create_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).filter(Usuario.estado == True).offset(skip).limit(limit).all()

def get_usuario_por_id(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.estado == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

def update_usuario(db: Session, usuario_id: int, datos: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.estado == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    campos_permitidos = {"nombres", "apellidos", "email", "password"}

    for key, value in datos.model_dump(exclude_unset=True).items():
        if key not in campos_permitidos:
            continue
        else:
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

def delete_usuario_logico(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=400, detail="Usuario ya desactivado")
    
    usuario.estado = False
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} eliminado (lógicamente)"}

def recuperar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == True:
        raise HTTPException(status_code=400, detail="Usuario ya activado")
    
    usuario.estado = True
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} recuperado"}

def delete_usuario_fisico(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario: {usuario.nombres} {usuario.apellidos} eliminado (físicamente)"}