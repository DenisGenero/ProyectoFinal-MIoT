from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.comederos import ComederoCreate, ComederoRead
from app.crud import comederos as crud

router = APIRouter()

@router.post("/comederos/", response_model=ComederoRead)
def crear_comedero(comedero: ComederoCreate, db: Session = Depends(get_db)):
    return crud.create_comedero(db, comedero)

@router.get("/comederos/", response_model=list[ComederoRead])
def listar_comederos(db: Session = Depends(get_db)):
    return crud.get_comederos(db)

@router.get("/comederos/{comedero_id}", response_model=ComederoRead)
def obtener_comedero(comedero_id: int, db: Session = Depends(get_db)):
    db_comedero = crud.get_comedero(db, comedero_id)
    if db_comedero is None:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    return db_comedero

@router.delete("/comederos/{comedero_id}")
def eliminar_comedero(comedero_id: int, db: Session = Depends(get_db)):
    db_comedero = crud.delete_comedero(db, comedero_id)
    if db_comedero is None:
        raise HTTPException(status_code=404, detail="Comedero no encontrado")
    return {"ok": True}
