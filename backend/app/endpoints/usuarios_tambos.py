from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.usuarios_tambos import asociar_usuario_tambo, eliminar_usuario_tambo

router = APIRouter()

@router.post("/usuarios/{id_usuario}/tambos/{id_tambo}")
def asociar_usuario(id_usuario: int, id_tambo: int, db: Session = Depends(get_db)):
    return asociar_usuario_tambo(db, id_usuario, id_tambo)

@router.delete("/usuarios/{id_usuario}/tambos/{id_tambo}")
def eliminar_usuario(id_usuario: int, id_tambo: int, db: Session = Depends(get_db)):
    return eliminar_usuario_tambo(db, id_usuario, id_tambo)

@router.get("/usuarios/{id_usuario}/tambos")
def obtener_tambos_de_usuario(id_usuario: int, db: Session = Depends(get_db)):
    from app.models.tambos import Tambo
    from app.models.usuarios_tambos import UsuarioTambo
    tambos = (
        db.query(Tambo)
        .join(UsuarioTambo, UsuarioTambo.id_tambo == Tambo.id)
        .filter(UsuarioTambo.id_usuario == id_usuario)
        .all()
    )
    return tambos

@router.get("/tambos/{id_tambo}/usuarios")
def obtener_usuarios_de_tambo(id_tambo: int, db: Session = Depends(get_db)):
    from app.models.usuarios import Usuario
    from app.models.usuarios_tambos import UsuarioTambo
    usuarios = (
        db.query(Usuario)
        .join(UsuarioTambo, UsuarioTambo.id_usuario == Usuario.id)
        .filter(UsuarioTambo.id_tambo == id_tambo)
        .all()
    )
    return usuarios