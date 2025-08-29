from sqlalchemy.orm import Session
from app.models.roles import Rol
from app.schemas.roles import RolCreate, UpdateRol
from fastapi import HTTPException

def create_rol(db: Session, rol: RolCreate):
    rol_nuevo = Rol(**rol.model_dump())
    rol_nuevo.estado = True
    db.add(rol_nuevo)
    db.commit()
    db.refresh(rol_nuevo)
    return rol_nuevo

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    rol = db.query(Rol).filter(Rol.estado == True).offset(skip).limit(limit).all()
    if not rol:
        raise HTTPException(status_code=404, detail="Roles no encontrados")
    
    return rol

def get_rol_por_id(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.estado == True).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Roles no encontrados")
    if rol.estado == False:
        raise HTTPException(status_code=400, detail="Rol inactivo")
    
    return rol

def update_rol(db: Session, rol_id: int, rol_data: UpdateRol) -> Rol:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if rol.estado == False:
        raise HTTPException(status_code=400, detail="Rol inactivo")
    
    campos_permitidos: {"nombre"}
    update_data = rol_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if not key in campos_permitidos:
            continue
        if len(value) == 0:
            continue
        setattr(rol, key, value)

    db.commit()
    db.refresh(rol)
    return rol

def deactivate_rol(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if rol.estado == False:
        raise HTTPException(status_code=400, detail="Rol ya desactivado")
    
    rol.estado = False
    db.commit()
    db.refresh(rol)
    return {"mensaje:" f"Rol: {rol.nombre} desactivado"}

def activate_rol(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if rol.estado == True:
        raise HTTPException(status_code=400, detail="Rol ya activado")
    
    rol.estado = True
    db.commit()
    db.refresh(rol)
    return {"mensaje:" f"Rol: {rol.nombre} activado"}

def delete_rol(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    db.delete(rol)
    db.commit()
    return{"mensaje": f"Rol: {rol.nombre} eliminado"}
