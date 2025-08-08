from sqlalchemy.orm import Session
from app.models.usuarios_tambos import UsuarioTambo

def asociar_usuario_tambo(db: Session, id_usuario: int, id_tambo: int):
    relacion = UsuarioTambo(id_usuario=id_usuario, id_tambo=id_tambo)
    db.add(relacion)
    db.commit()
    return {"mensaje": "Usuario asociado al tambo"}

def eliminar_usuario_tambo(db: Session, id_usuario: int, id_tambo: int):
    relacion = db.query(UsuarioTambo).filter_by(id_usuario=id_usuario, id_tambo=id_tambo).first()
    if not relacion:
        raise Exception("La relación no existe")
    db.delete(relacion)
    db.commit()
    return {"mensaje": "Asociación eliminada"}
