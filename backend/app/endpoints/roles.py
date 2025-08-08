from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.roles import RolCreate, RolRead
from app.crud import roles as crud_roles

#router = APIRouter(prefix="/roles", tags=["roles"])
router = APIRouter()

@router.get("/", response_model=list[RolRead])
def listar_roles(db: Session = Depends(get_db)):
    return crud_roles.get_roles(db)

@router.get("/{rol_id}", response_model=RolRead)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = crud_roles.get_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/", response_model=RolRead)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return crud_roles.create_rol(db, rol)

@router.delete("/{rol_id}", response_model=RolRead)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = crud_roles.delete_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
