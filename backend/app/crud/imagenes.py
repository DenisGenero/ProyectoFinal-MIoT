from sqlalchemy.orm import Session
from app.models.imagenes import Imagen
from app.schemas.imagenes import ImagenCreate, UpdateImagen
from fastapi import HTTPException

def create_imagen(db: Session, imagen: ImagenCreate):
    imagen_nueva = Imagen(**imagen.dict())
    db.add(imagen_nueva)
    db.commit()
    db.refresh(imagen_nueva)
    return imagen_nueva

def get_imagenes(db: Session, skip: int = 0, limit: int = 100):
    imagenes = db.query(Imagen).offset(skip).limit(limit).all()
    if not imagenes:
        raise HTTPException(status_code=404, detail="Imageness no encontradas")
    return imagenes

def get_imagenes_por_id(db: Session, imagen_id: int):
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return imagen

def get_imagenes_dispositivo(db: Session, dispositivo_id):
    imagenes = db.query(Imagen).filter(Imagen.id_dispositivo == dispositivo_id).all()

    return imagenes

def update_imagen(db: Session, imagen_id: int, imagen_data: UpdateImagen):
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    campos_permitidos = {"path_imagen"}
    update_data = imagen_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
    for key, value in update_data.items():
        if key not in campos_permitidos:
            continue
        if len(value) == 0:
            continue
        setattr(imagen, key, value)
    
    db.commit()
    db.refresh(imagen)
    return imagen

def delete_imagen(db: Session, imagen_id: int):
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    db.delete(imagen)
    db.commit()
    return {"mensaje": f"Imagen: {imagen.id} eliminada"}
