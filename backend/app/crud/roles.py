from sqlalchemy.orm import Session
from app.models.roles import Rol
from app.schemas.roles import RolCreate, UpdateRol
from fastapi import HTTPException

def get_roles(db: Session):
    return db.query(Rol).all()

def get_rol(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.id == rol_id).first()

def create_rol(db: Session, rol: RolCreate):
    db_rol = Rol(nombre=rol.nombre, es_admin=rol.es_admin)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db: Session, rol_id: int, rol_data: UpdateRol) -> Rol:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    update_data = rol_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if len(value) == 0:
            continue
        setattr(rol, key, value)

    db.commit()
    db.refresh(rol)
    return rol

def delete_rol(db: Session, rol_id: int):
    db_rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol
