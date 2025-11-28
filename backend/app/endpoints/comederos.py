from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.comederos import ComederoCreate, ComederoRead, UpdateComedero
from app.crud import comederos as crud_comederos
from app.core import security as security
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()

@router.post("/comederos/", response_model=ComederoRead)
def crear_comedero(
    comedero: ComederoCreate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_admin_en_tambo(db, comedero.id_tambo, token)

    return crud_comederos.create_comedero(db, comedero)

@router.get("/comederos/", response_model=list[ComederoRead])
def listar_comederos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_comederos.get_comederos(db, skip, limit)

@router.get("/comederos/{comedero_id}", response_model=ComederoRead)
def obtener_comedero(comedero_id: int, db: Session = Depends(get_db)):
    return crud_comederos.get_comedero_por_id(db, comedero_id)

@router.get("/comederos/{tambo_id}/tambo", response_model=list[ComederoRead])
def obtener_comederos_tambo(
    tambo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    current_user = security.get_usuario_from_token(db, token)
    security.ususario_pertenece_tambo(db, tambo_id, current_user)

    return crud_comederos.get_comederos_tambo(db, tambo_id)

@router.put("/comederos/{comedero_id}", response_model=ComederoRead)
def actualizar_comedero(
    comedero_id: int,
    comedero_data: UpdateComedero,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id: int = crud_comederos.get_tambo_id_comedero(db, comedero_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_comederos.update_comedero(db, comedero_id, comedero_data)

@router.put("/comederos/{comedero_id}/desactivar")
def desactivar_comedero(
    comedero_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id: int = crud_comederos.get_tambo_id_comedero(comedero_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_comederos.deactivate_comedero(db, comedero_id)

@router.put("/comederos/{comedero_id}/recuperar")
def activar_comedero(
    comedero_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id: int = crud_comederos.get_tambo_id_comedero(comedero_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_comederos.activate_comedero(db, comedero_id)

@router.delete("/comederos/{comedero_id}")
def eliminar_comedero(
    comedero_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_comederos.delete_comedero(db, comedero_id)
