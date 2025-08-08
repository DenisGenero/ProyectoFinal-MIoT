# app/crud/dispositivos.py

from sqlalchemy.orm import Session
from app.models.dispositivos import Dispositivo
from app.schemas.dispositivos import DispositivoCreate

def create_dispositivo(db: Session, dispositivo: DispositivoCreate):
    db_dispositivo = Dispositivo(**dispositivo.dict())
    db.add(db_dispositivo)
    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo

def get_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dispositivo).offset(skip).limit(limit).all()

def get_dispositivo(db: Session, dispositivo_id: int):
    return db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()

def delete_dispositivo(db: Session, dispositivo_id: int):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if dispositivo:
        db.delete(dispositivo)
        db.commit()
    return dispositivo
