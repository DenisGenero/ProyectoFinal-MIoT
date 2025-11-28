from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.usuarios import UsuarioRead, UsuarioUpdate
from app.crud import usuarios as crud_usuarios
from app.core.security import es_superadmin, get_usuario_from_token, oauth2_scheme
from fastapi.security import HTTPAuthorizationCredentials


router = APIRouter()

@router.get("/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    es_superadmin(db, token)
    
    return crud_usuarios.get_usuarios(db, skip, limit)


@router.get("/usuarios/buscar_por_mail", response_model=UsuarioRead)
def obtener_usuario_mail(
   email: str,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    get_usuario_from_token(db, token)
    
    return crud_usuarios.get_usuario_por_mail(db, email)


@router.get("/usuarios/me", response_model=UsuarioRead)
def obtener_usuario_token(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print(token)
    return get_usuario_from_token(db, token)
    #print(usuario.apellidos)
    #return usuario


@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud_usuarios.get_usuario_por_id(db, usuario_id)

@router.put("/usuarios/actualiza_mismo_usuario", response_model=UsuarioRead)
def actualizar_propio_usuario(
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print("Data usuario: ", usuario_data)
    current_user = get_usuario_from_token(db, token)
    
    return crud_usuarios.update_usuario(db, current_user.id, usuario_data)


@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    es_superadmin(db, token)
    
    return crud_usuarios.update_usuario(db, usuario_id, usuario_data)


@router.put("/usuarios/{usuario_id}/desactivar")
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    es_superadmin(db, token)
    
    return crud_usuarios.deactivate_usuario(db, usuario_id)


@router.put("/usuarios/{usuario_id}/recuperar")
def activar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    es_superadmin(db, token)

    return crud_usuarios.activate_usuario(db, usuario_id)


@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    es_superadmin(db, token)
    
    return crud_usuarios.delete_usuario(db, usuario_id)
