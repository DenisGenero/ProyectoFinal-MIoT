from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.tambos import Tambo
from app.schemas.tambos import TamboCreate, TamboUpdate


def create_tambo(db: Session, tambo: TamboCreate) -> Tambo:
    db_tambo = Tambo(**tambo.model_dump())
    db.add(db_tambo)
    db.commit()
    db.refresh(db_tambo)
    return db_tambo


def get_tambos(db: Session):
    tambo = db.query(Tambo).filter(Tambo.estado == True).all() 
    return tambo


def get_tambo_by_id(db: Session, tambo_id: int) -> Tambo:
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo desactivado")
    return tambo


def update_tambo(db: Session, tambo_id: int, tambo_data: TamboUpdate) -> Tambo:
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo no activado")

    update_data = tambo_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
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
    if tambo.estado is False:
        raise HTTPException(status_code=400, detail="Tambo ya está desactivado")

    tambo.estado = False
    db.commit()
    db.refresh(tambo)
    return {"mensaje": f"Tambo {tambo.nombre} desactivado correctamente"}


def activate_tambo(db: Session, tambo_id: int):
    tambo = db.query(Tambo).filter(Tambo.id == tambo_id).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado is True:
        raise HTTPException(status_code=400, detail="Tambo ya está activo")

    tambo.estado = True
    db.commit()
    db.refresh(tambo)
    return {"mensaje": f"Tambo {tambo.nombre} activado correctamente"}

