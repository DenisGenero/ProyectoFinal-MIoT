from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.usuarios import Usuario
from app.models.tambos import Tambo
from app.models.roles import Rol
from app.models.usuarios_tambos_roles import UsuarioTamboRol
from app.schemas.usuarios_tambos_roles import UsuarioTamboRolCreate


# Asociar usuario con rol a un tambo
def asociar_usuario_tambo_rol(db: Session, asociacion: UsuarioTamboRolCreate):
    # Verificar existencia y estado de usuario
    usuario = db.query(Usuario).filter(Usuario.id == asociacion.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # Verificar existencia y estado de tambo
    tambo = db.query(Tambo).filter(Tambo.id == asociacion.id_tambo).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo inactivo")

    # Verificar existencia de rol
    rol = db.query(Rol).filter(Rol.id == asociacion.id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Buscar si ya existe una asociación
    existente = db.query(UsuarioTamboRol).filter(
        UsuarioTamboRol.id_usuario == asociacion.id_usuario,
        UsuarioTamboRol.id_tambo == asociacion.id_tambo
    ).first()

    # Si estaba deshabilitada, se reactiva
    if existente:
        if not existente.estado:
            existente.estado = True
            existente.id_rol = asociacion.id_rol
            db.commit()
            db.refresh(existente)
            return existente
        else:
            raise HTTPException(status_code=400, detail="La asociación ya existe")

    nueva_asociacion = UsuarioTamboRol(**asociacion.model_dump())
    db.add(nueva_asociacion)
    db.commit()
    db.refresh(nueva_asociacion)
    return nueva_asociacion


# Eliminar asociación (lógico)
def eliminar_usuario_tambo_rol_logico(db: Session, id_usuario: int, id_tambo: int):
    asociacion = db.query(UsuarioTamboRol).filter(
        UsuarioTamboRol.id_usuario == id_usuario,
        UsuarioTamboRol.id_tambo == id_tambo,
    ).first()
    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    if asociacion.estado == False:
        raise HTTPException(status_code=400, detail="Asociación ya eliminada")

    asociacion.estado = False
    db.commit()
    return {"mensaje": "Asociación: eliminada (lógicamente)"}

def recuperar_usuario_tambo_rol(db: Session, id_usuario: int, id_tambo: int):
    asociacion = db.query(UsuarioTamboRol).filter(
        UsuarioTamboRol.id_usuario == id_usuario,
        UsuarioTamboRol.id_tambo == id_tambo,
    ).first()

    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada o ya eliminada")
    if asociacion.estado == True:
        raise HTTPException(status_code=400, detail="Asociación ya activada")

    asociacion.estado = True
    db.commit()
    return {"mensaje": "Asociación restaurada"}

# Eliminar asociación (físico)
def eliminar_usuario_tambo_rol_fisico(db: Session, id_usuario: int, id_tambo: int):
    asociacion = db.query(UsuarioTamboRol).filter(
        UsuarioTamboRol.id_usuario == id_usuario,
        UsuarioTamboRol.id_tambo == id_tambo
    ).first()

    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")

    db.delete(asociacion)
    db.commit()
    return {"mensaje": "Asociación eliminada definitivamente"}


# Obtener usuarios y roles de un tambo
def get_usuarios_por_tambo(db: Session, id_tambo: int):
    tambo = db.query(Tambo).filter(Tambo.id == id_tambo).first()
    if not tambo:
        raise HTTPException(status_code=404, detail="Tambo no encontrado")
    if tambo.estado == False:
        raise HTTPException(status_code=400, detail="Tambo inactivo")

    asociaciones = db.query(UsuarioTamboRol).options(joinedload(UsuarioTamboRol.usuario), joinedload(UsuarioTamboRol.rol)).filter(
        UsuarioTamboRol.id_tambo == id_tambo,
        UsuarioTamboRol.estado == True,
        Usuario.estado == True
    ).join(Usuario, UsuarioTamboRol.id_usuario == Usuario.id).all()

    return asociaciones


# Obtener tambos y roles de un usuario
def get_tambos_por_usuario(db: Session, id_usuario: int):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.estado == False:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    asociaciones = db.query(UsuarioTamboRol).options(joinedload(UsuarioTamboRol.tambo), joinedload(UsuarioTamboRol.rol)).filter(
        UsuarioTamboRol.id_usuario == id_usuario,
        UsuarioTamboRol.estado == True,
        Tambo.estado == True
    ).join(Tambo, UsuarioTamboRol.id_tambo == Tambo.id).all()

    return asociaciones
