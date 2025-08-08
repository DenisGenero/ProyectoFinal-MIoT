from sqlalchemy.orm import Session
from app.models.tambos import Tambo
from app.schemas.tambos import TamboCreate

def create_tambo(db: Session, tambo: TamboCreate) -> Tambo:
    db_tambo = Tambo(**tambo.dict())
    db.add(db_tambo)
    db.commit()
    db.refresh(db_tambo)
    return db_tambo

def get_tambos(db: Session):
    return db.query(Tambo).all()
