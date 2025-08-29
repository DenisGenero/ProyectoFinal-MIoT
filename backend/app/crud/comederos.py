from sqlalchemy.orm import Session
from app.models.comederos import Comedero
from app.schemas.comederos import ComederoCreate, UpdateComedero
from fastapi import HTTPException

def create_comedero(db: Session, comedero: ComederoCreate):
    comedero_nuevo = Comedero(**comedero.model_dump())
    comedero_nuevo.estado = True
    db.add(comedero_nuevo)
    db.commit()
    db.refresh(comedero_nuevo)
    return comedero_nuevo

def get_comederos(db: Session, skip: int = 0, limit: int = 100):
    comederos = db.query(Comedero).filter(Comedero.estado == True).offset(skip).limit(limit).all()
    if not comederos:
        raise HTTPException(status_code=404, detail="Comederos no encontrados")
    
    return comederos

def get_comedero_por_id(db: Session, comedero_id: int):
    comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if not comedero:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    if comedero.estado == False:
        raise HTTPException(status_code=400, detail="Comedero inactivo")
    
    return comedero

def get_comederos_tambo(db: Session, tambo_id: int):
    comederos = db.query(Comedero).filter(Comedero.id_tambo == tambo_id, Comedero.estado == True).all()
    if not comederos:
        raise HTTPException(status_code=404, detail="Comederos no encontrados")
    
    return comederos

def update_comedero(db: Session, comedero_id: int, comedero_data: UpdateComedero):
    comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if not comedero:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    if comedero.estado == False:
        raise HTTPException(status_code=400, detail="Comedero inactivo")
    
    campos_permitidos = {"nombre", "descripcion", "ubicacion"}
    update_data = comedero_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if key not in campos_permitidos:
            continue
        if len(value) == 0:
            continue
        setattr(comedero, key, value)

    db.commit()
    db.refresh(comedero)
    return comedero

def deactivate_comedero(db: Session, comedero_id: int):
    comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if not comedero:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    if comedero.estado == False:
        raise HTTPException(status_code=400, detail="Comedero ya desactivado")
    
    comedero.estado = False
    db.commit()
    db.refresh(comedero)
    return {"mensaje:" f"Comedero: {comedero.nombre} desactivado"}

def activate_comedero(db: Session, comedero_id: int):
    comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if not comedero:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    if comedero.estado == True:
        raise HTTPException(status_code=400, detail="Comedero ya activado")
    
    comedero.estado = True
    db.commit()
    db.refresh(comedero)
    return {"mensaje:" f"Comedero: {comedero.nombre} activado"}

def delete_comedero(db: Session, comedero_id: int):
    comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if not comedero:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
        
    db.delete(comedero)
    db.commit()
    return {"mensaje": f"Comedero: {comedero.nombre} eliminado"}
