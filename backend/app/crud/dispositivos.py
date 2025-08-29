from sqlalchemy.orm import Session
from app.models.dispositivos import Dispositivo
from app.schemas.dispositivos import DispositivoCreate, UpdateDispositivo
from fastapi import HTTPException

def create_dispositivo(db: Session, dispositivo: DispositivoCreate):
    dispositivo_nuevo = Dispositivo(**dispositivo.model_dump())
    dispositivo_nuevo.estado = True
    db.add(dispositivo_nuevo)
    db.commit()
    db.refresh(dispositivo_nuevo)
    return dispositivo_nuevo

def get_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    dispositivos =  db.query(Dispositivo).filter(Dispositivo.estado == True).offset(skip).limit(limit).all()
    if not dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivos no encontrados")
    
    return dispositivos

def get_dispositivo_por_id(db: Session, dispositivo_id: int):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if dispositivo.estado == False:
        raise HTTPException(status_code=400, detail="Dispositivo inactivo")
    
    return dispositivo

def get_dispositivos_comedero(db: Session, comedero_id):
    dispositivos = db.query(Dispositivo).filter(Dispositivo.id_comedero == comedero_id, Dispositivo.estado == True).all()
    if not dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivos no encontrados")
    
    return dispositivos

def update_dispositivo(db: Session, dispositivo_id: int, dispositivo_data: UpdateDispositivo):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if dispositivo.estado == False:
        raise HTTPException(status_code=400, detail="Dispositivo inactivo")
    
    campos_permitidos = {"nombre", "usuario_local", "direccion_local", "puerto_ssh", 
                         "usuario_servidor", "direccion_servidor", "puerto_servidor",
                         "hora_inicio", "hora_fin", "intervalo"}
    update_data = dispositivo_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if key not in campos_permitidos:
            continue
        if len(value) == 0:
            continue
        setattr(dispositivo, key, value)

    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def deactivate_dispositivo(db: Session, dispositivo_id: int):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if dispositivo.estado == False:
        raise HTTPException(status_code=400, detail="Dispositivo ya desactivado")
    
    dispositivo.estado = False
    db.commit()
    db.refresh(dispositivo)
    return {"mensaje:" f"Dispositivo: {dispositivo.nombre} desactivado"}

def activate_dispositivo(db: Session, dispositivo_id: int):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if dispositivo.estado == True:
        raise HTTPException(status_code=400, detail="Dispositivo ya activado")
    
    dispositivo.estado = True
    db.commit()
    db.refresh(dispositivo)
    return {"mensaje:" f"Dispositivo: {dispositivo.nombre} activado"}

def delete_dispositivo(db: Session, dispositivo_id: int):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db.delete(dispositivo)
    db.commit()
    return dispositivo
