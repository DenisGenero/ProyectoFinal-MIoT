from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
import app.crud.usuarios_tambos_roles as crud_utr

router = APIRouter()

# Asociar un usuario a un tambo
@router.post("/usuarios/{id_usuario}/tambos/{id_tambo}")
def asociar_usuario(id_usuario: int, id_tambo: int, db: Session = Depends(get_db)):
    return crud_utr.asociar_usuario_tambo_rol(db, id_usuario, id_tambo)

# Borrado físico de un usuario en un tambo
@router.delete("/usuarios/{id_usuario}/tambos/{id_tambo}")
def eliminar_usuario(id_usuario: int, id_tambo: int, db: Session = Depends(get_db)):
    return crud_utr.eliminar_usuario_tambo_rol_fisico(db, id_usuario, id_tambo)

# Borrado lógico de un usuario en un tambo
@router.put("/usuarios-tambos-roles/{usuario_id}/{tambo_id}/desactivar")
def desactivar_usuario_tambo_rol(usuario_id: int, tambo_id: int, db: Session = Depends(get_db)):
    return crud_utr.eliminar_usuario_tambo_rol_logico(db, usuario_id, tambo_id)

# Revertir borrado lógico
@router.put("/usuarios-tambos-roles/{usuario_id}/{tambo_id}/reactivar")
def reactivar_usuario_tambo_rol(usuario_id: int, tambo_id: int, db: Session = Depends(get_db)):
    return crud_utr.recuperar_usuario_tambo_rol(db, usuario_id, tambo_id)

# Obtener tambos de un usuario
@router.get("/usuarios/{usuario_id}/tambos")
def obtener_tambos_de_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_utr.get_tambos_por_usuario(db, usuario_id)

# Obtener los usuarios de un tambo
@router.get("/tambos/{tambo_id}/usuarios")
def obtener_usuarios_de_tambo(tambo_id: int, db: Session = Depends(get_db)):
    return crud_utr.get_usuarios_por_tambo(db, tambo_id)