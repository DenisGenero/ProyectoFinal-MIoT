from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.tambos import TamboCreate, TamboRead, TamboUpdate
from app.crud import tambos as crud_tambos

router = APIRouter()

# Crear un tambo
@router.post("/tambos/", response_model=TamboRead)
def crear_tambo(tambo: TamboCreate, db: Session = Depends(get_db)):
    return crud_tambos.create_tambo(db, tambo)


# Listar tambos activos
@router.get("/tambos/", response_model=list[TamboRead])
def listar_tambos(db: Session = Depends(get_db)):
    return crud_tambos.get_tambos(db)


# Obtener un tambo por ID
@router.get("/tambos/{tambo_id}", response_model=TamboRead)
def obtener_tambo(tambo_id: int, db: Session = Depends(get_db)):
    return crud_tambos.get_tambo_by_id(db, tambo_id)


# Actualizar un tambo
@router.put("/tambos/{tambo_id}", response_model=TamboRead)
def actualizar_tambo(tambo_id: int, tambo: TamboUpdate, db: Session = Depends(get_db)):
    return crud_tambos.update_tambo(db, tambo_id, tambo)


# Desactivar un tambo
@router.put("/tambos/{tambo_id}/desactivar")
def desactivar_tambo(tambo_id: int, db: Session = Depends(get_db)):
    return crud_tambos.deactivate_tambo(db, tambo_id)


# Activar un tambo
@router.put("/tambos/{tambo_id}/activar")
def activar_tambo(tambo_id: int, db: Session = Depends(get_db)):
    return crud_tambos.activate_tambo(db, tambo_id)

