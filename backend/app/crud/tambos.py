from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.tambos import Tambo
from app.schemas.tambos import TamboCreate, TamboUpdate


def create_tambo(db: Session, tambo: TamboCreate) -> Tambo:
    tambo_nuevo = Tambo(**tambo.model_dump())
    tambo_nuevo.estado = True
    db.add(tambo_nuevo)
    db.commit()
    db.refresh(tambo_nuevo)
    return tambo_nuevo


def get_todos_tambos(db: Session, skip: int = 0, limit: int = 100):
    tambos = db.query(Tambo).offset(skip).limit(limit).all() 
    if not tambos:
        raise HTTPException(status_code=404, detail="Tambos no encontrados")
    
    return tambos


def get_tambos_activos(db: Session, skip: int = 0, limit: int = 100):
    tambos = db.query(Tambo).filter(Tambo.estado == True).offset(skip).limit(limit).all() 
    if not tambos:
        raise HTTPException(status_code=404, detail="Tambos no encontrados")
    
    return tambos

def get_tambo_por_id(db: Session, tambo_id: int) -> Tambo:
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo inactivo")
    return tambo

def update_tambo(db: Session, tambo_id: int, tambo_data: TamboUpdate) -> Tambo:
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo inactivo")
    
    campos_permitidos = {"nombre", "descricion", "ubicacion"}
    update_data = tambo_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if key not in campos_permitidos:
            continue
        if len(value) == 0:
            continue
        setattr(tambo, key, value)

    db.commit()
    db.refresh(tambo)
    return tambo


def deactivate_tambo(db: Session, tambo_id: int):
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo ya está desactivado")

    tambo.estado = False
    db.commit()
    db.refresh(tambo)
    return {"mensaje": f"Tambo {tambo.nombre} desactivado correctamente"}


def activate_tambo(db: Session, tambo_id: int):
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == True:
        raise HTTPException(status_code=400, detail="Tambo ya está activo")

    tambo.estado = True
    db.commit()
    db.refresh(tambo)
    return {"mensaje": f"Tambo {tambo.nombre} activado correctamente"}

def delete_tambo(db: Session, tambo_id: int):
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
        
    db.delete(tambo)
    db.commit()
    return {"mensaje": f"Tambo: {tambo.nombre} eliminado"}