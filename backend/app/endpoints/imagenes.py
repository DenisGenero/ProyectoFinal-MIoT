from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.imagenes import Imagen
from app.schemas.imagenes import ImagenCreate, ImagenRead, UpdateImagen 
from app.crud import imagenes as crud_imagenes
from app.crud import dispositivos as crud_dispositivos
from app.core import security as security
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()

@router.post("/imagenes/", response_model=ImagenRead)
def crear_imagen(
    imagen: ImagenCreate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme_device)
    ):
    dispositivo = security.get_dispositivo_from_jwt(db, token)

    return crud_imagenes.create_imagen(db, imagen, dispositivo.id)

"""
@router.get("/imagenes/", response_model=list[ImagenRead])
def listar_imagenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_imagenes.get_imagenes(db, skip, limit)
""" 

@router.get("/imagenes/{imagen_id}", response_model=ImagenRead)
def obtener_imagen(
    imagen_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)
    ):
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    usuario = security.get_usuario_from_token(db, token)
    tambo_id = crud_dispositivos.get_tambo_id_dispositivo(db, imagen.id_dispositivo)
    security.ususario_pertenece_tambo(db, tambo_id, usuario)

    return crud_imagenes.get_imagenes_por_id(db, imagen_id)

@router.get("/imagenes/dispositivo/{dispositivo_id}", response_model=list[ImagenRead])
def obtener_imagenes_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)
    ):
    usuario = security.get_usuario_from_token(db, token)
    tambo_id = crud_dispositivos.get_tambo_id_dispositivo(db, dispositivo_id)
    security.ususario_pertenece_tambo(db, tambo_id, usuario)

    return crud_imagenes.get_imagenes_dispositivo(db, dispositivo_id)

@router.put("/imagenes/{imagen_id}", response_model=ImagenRead)
def actualizar_imagen(
    imagen_id: int,
    imagen_data: UpdateImagen,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_imagenes.update_imagen(db, imagen_id, imagen_data)

@router.delete("/imagenes/{imagen_id}")
def eliminar_imagen(
    imagen_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)
    
    crud_imagenes.delete_imagen(db, imagen_id)
