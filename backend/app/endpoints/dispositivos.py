from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.dispositivos import DispositivoCreate, DispositivoRead
from app.crud import dispositivos as crud_dispositivos

router = APIRouter()

@router.post("/dispositivos/", response_model=DispositivoRead)
def crear_dispositivo(dispositivo: DispositivoCreate, db: Session = Depends(get_db)):
    return crud_dispositivos.create_dispositivo(db, dispositivo)

@router.get("/dispositivos/", response_model=list[DispositivoRead])
def listar_dispositivos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_dispositivos.get_dispositivos(db, skip, limit)

@router.get("/dispositivos/{dispositivo_id}", response_model=DispositivoRead)
def obtener_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    db_dispositivo = crud_dispositivos.get_dispositivo(db, dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db_dispositivo

@router.delete("/dispositivos/{dispositivo_id}", response_model=DispositivoRead)
def eliminar_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    db_dispositivo = crud_dispositivos.delete_dispositivo(db, dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db_dispositivo
