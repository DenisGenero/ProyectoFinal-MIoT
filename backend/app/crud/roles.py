from sqlalchemy.orm import Session
from app.models.roles import Rol
from app.schemas.roles import RolCreate

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

def delete_rol(db: Session, rol_id: int):
    db_rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol
