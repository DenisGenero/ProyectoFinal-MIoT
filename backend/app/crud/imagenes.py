from sqlalchemy.orm import Session
from app.models.imagenes import Imagen
from app.schemas.imagenes import ImagenCreate

def create_imagen(db: Session, imagen: ImagenCreate):
    db_imagen = Imagen(**imagen.dict())
    db.add(db_imagen)
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def get_imagenes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Imagen).offset(skip).limit(limit).all()

def get_imagenes_por_dispositivo(db: Session, dispositivo_id: int):
    return db.query(Imagen).filter(Imagen.id_dispositivo == dispositivo_id).all()

def delete_imagen(db: Session, imagen_id: int):
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    if imagen:
        db.delete(imagen)
        db.commit()
    return imagen
