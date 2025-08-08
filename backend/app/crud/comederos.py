from sqlalchemy.orm import Session
from app.models.comederos import Comedero
from app.schemas.comederos import ComederoCreate

def create_comedero(db: Session, comedero: ComederoCreate):
    db_comedero = Comedero(**comedero.dict())
    db.add(db_comedero)
    db.commit()
    db.refresh(db_comedero)
    return db_comedero

def get_comederos(db: Session):
    return db.query(Comedero).all()

def get_comedero(db: Session, comedero_id: int):
    return db.query(Comedero).filter(Comedero.id == comedero_id).first()

def delete_comedero(db: Session, comedero_id: int):
    db_comedero = db.query(Comedero).filter(Comedero.id == comedero_id).first()
    if db_comedero:
        db.delete(db_comedero)
        db.commit()
    return db_comedero
