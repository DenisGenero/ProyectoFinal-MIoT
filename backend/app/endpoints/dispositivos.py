from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.dispositivos import DispositivoCreate, DispositivoRead, UpdateDispositivo
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
    return crud_dispositivos.get_dispositivo_por_id(db, dispositivo_id)

@router.get("/dispositivos/{comedero_id}/comedero", response_model=list[DispositivoRead])
def obtener_dispositivos_comedero(comedero_id: int, db: Session = Depends(get_db)):
    return crud_dispositivos.get_dispositivos_comedero(db, comedero_id)

@router.put("/dispositivos/{dispositivo_id}", response_model=DispositivoRead)
def actualizar_dispositivo(dispositivo_id: int, dispositivo_data: UpdateDispositivo, db: Session = Depends(get_db)):
    return crud_dispositivos.update_dispositivo(db, dispositivo_id, dispositivo_data)

@router.put("/dispositivos/{dispositivo_id}/desactivar")
def desactivar_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    return crud_dispositivos.deactivate_dispositivo(db, dispositivo_id)

@router.put("/dispositivos/{dispositivo_id}/recuperar")
def recuperar_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    return crud_dispositivos.activate_dispositivo(db, dispositivo_id)

@router.delete("/dispositivos/{dispositivo_id}", response_model=DispositivoRead)
def eliminar_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    return crud_dispositivos.delete_dispositivo(db, dispositivo_id)
