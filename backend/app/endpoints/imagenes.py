from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.imagenes import ImagenCreate, ImagenRead, UpdateImagen 
from app.crud import imagenes as crud_imagenes

router = APIRouter()

@router.post("/imagenes/", response_model=ImagenRead)
def crear_imagen(imagen: ImagenCreate, db: Session = Depends(get_db)):
    return crud_imagenes.create_imagen(db, imagen)

@router.get("/imagenes/", response_model=list[ImagenRead])
def listar_imagenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_imagenes.get_imagenes(db, skip, limit)

@router.get("/imagenes/{imagen_id}", response_model=ImagenRead)
def obtener_imagen(imagen_id: int, db: Session = Depends(get_db)):
    return crud_imagenes.get_imagenes_por_id(db, imagen_id)

@router.get("/imagenes/dispositivo/{id_dispositivo}", response_model=list[ImagenRead])
def obtener_imagenes_dispositivo(id_dispositivo: int, db: Session = Depends(get_db)):
    return crud_imagenes.get_imagenes_dispositivo(db, id_dispositivo)

@router.put("/imagenes/{imagen_id}", response_model=ImagenRead)
def actualizar_imagen(imagen_id: int, imagen_data: UpdateImagen, db: Session = Depends(get_db)):
    return crud_imagenes.update_imagen(db, imagen_id, imagen_data)

@router.delete("/imagenes/{imagen_id}")
def eliminar_imagen(imagen_id: int, db: Session = Depends(get_db)):
    imagen = crud_imagenes.delete_imagen(db, imagen_id)
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return {"ok": True}

