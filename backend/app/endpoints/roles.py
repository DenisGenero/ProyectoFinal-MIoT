from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.roles import RolCreate, RolRead, UpdateRol
from app.crud import roles as crud_roles

router = APIRouter()

@router.post("/roles/", response_model=RolRead)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return crud_roles.create_rol(db, rol)

@router.get("/roles/", response_model=list[RolRead])
def listar_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_roles.get_roles(db, skip, limit)

@router.get("/roles/{rol_id}", response_model=RolRead)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    return crud_roles.get_rol_por_id(db, rol_id)

@router.put("/roles/{rol_id}", response_model=RolRead)
def actualizar_rol(rol_id: int, rol: UpdateRol, db: Session = Depends(get_db)):
    return crud_roles.update_rol(db, rol_id, rol)

@router.put("/roles/{rol_id}/desactivar")
def desactivar_rol(rol_id: int, db: Session = Depends(get_db)):
    return crud_roles.deactivate_rol(db, rol_id)

@router.put("/roles/{rol_id}/recuperar")
def activar_rol(rol_id: int, db: Session = Depends(get_db)):
    return crud_roles.activate_rol(db, rol_id)

@router.delete("/roles/{rol_id}", response_model=RolRead)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = crud_roles.delete_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
