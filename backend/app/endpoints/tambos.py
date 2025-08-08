from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.tambos import TamboCreate, TamboRead
from app.crud import tambos as crud_tambos

router = APIRouter()

@router.post("/tambos/", response_model=TamboRead)
def crear_tambo(tambo: TamboCreate, db: Session = Depends(get_db)):
    return crud_tambos.create_tambo(db, tambo)

@router.get("/tambos/", response_model=list[TamboRead])
def listar_tambos(db: Session = Depends(get_db)):
    return crud_tambos.get_tambos(db)
