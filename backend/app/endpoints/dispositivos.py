from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.dispositivos import DispositivoCreate, DispositivoConfigRead, DispositivoAdminRead, UpdateDispositivo, UpdateDispositivoAdmin
from app.crud import dispositivos as crud_dispositivos
from app.core import security as security
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()

@router.post("/dispositivos/", response_model=DispositivoConfigRead)
def crear_dispositivo(
    dispositivo: DispositivoCreate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id = crud_dispositivos.get_tambo_id_comedero(db, dispositivo.id_comedero)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_dispositivos.create_dispositivo(db, dispositivo)

@router.get("/dispositivos", response_model=list[DispositivoAdminRead])
def listar_dispositivos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivos(db, skip, limit)

@router.get("/dispositivos/mac", response_model=DispositivoAdminRead)
def obtener_dispositivo_por_mac(
    mac_address: str,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivo_por_mac(db, mac_address)

@router.get("/dispositivos/rpi-config", response_model=DispositivoAdminRead)
def obtener_config_rpi(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme_device)
    ):
    dispositivo = security.get_dispositivo_from_jwt(db, token)

    return dispositivo

@router.get("/dispositivos/rpi-schedule", response_model=DispositivoConfigRead)
def obtener_schedule_rpi(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme_device)
    ):
    dispositivo = security.get_dispositivo_from_jwt(db, token)

    return dispositivo

@router.get("/dispositivos/{dispositivo_id}/config", response_model=DispositivoConfigRead, response_model_exclude={"admin_config"})
def obtener_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    current_user = security.get_usuario_from_token(db, token)
    dispositivo = crud_dispositivos.get_dispositivo_por_id(db, dispositivo_id)
    tambo_id = crud_dispositivos.get_tambo_id_comedero(db, dispositivo.id_comedero)
    security.ususario_pertenece_tambo(db, tambo_id, current_user)

    return crud_dispositivos.get_dispositivo_por_id(db, dispositivo_id)

@router.get("/dispositivos/usuario", response_model=list[DispositivoAdminRead], response_model_exclude={"config"})
def obtener_dispositivos_usuario(
    email: str,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.get_usuario_from_token(db, token)

    return crud_dispositivos.get_dispositivos_por_usuario(db, email)


@router.get("/dispositivos/{dispositivo_id}/admin-config", response_model=DispositivoAdminRead, response_model_exclude={"config"})
def obtener_dispositivo_admin(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivo_por_id(db, dispositivo_id)

@router.get("/dispositivos/{comedero_id}/comedero", response_model=list[DispositivoConfigRead])
def obtener_dispositivos_comedero(
    comedero_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    current_user = security.get_usuario_from_token(db, token)
    tambo_id = crud_dispositivos.get_tambo_id_comedero(db, comedero_id)
    security.ususario_pertenece_tambo(db, tambo_id, current_user)

    return crud_dispositivos.get_dispositivos_comedero(db, comedero_id)

@router.get("/dispositivos/sin-config", response_model=list[DispositivoAdminRead])
def obtener_dispositivos_sin_config(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivos_sin_config(db, skip=skip, limit=limit)


@router.get("/dispositivos/sin-config/tambo/{tambo_id}", response_model=list[DispositivoAdminRead])
def obtener_dispositivos_sin_config_por_tambo(
    tambo_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivos_sin_config_por_tambo(db, tambo_id, skip=skip, limit=limit)


@router.get("/dispositivos/sin-config/comedero/{comedero_id}", response_model=list[DispositivoAdminRead])
def obtener_dispositivos_sin_config_por_comedero(
    comedero_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.get_dispositivos_sin_config_por_comedero(db, comedero_id, skip=skip, limit=limit)


@router.put("/dispositivos/{dispositivo_id}/config", response_model=DispositivoConfigRead, response_model_exclude={"admin_config"})
def actualizar_dispositivo(
    dispositivo_id: int,
    dispositivo_data: UpdateDispositivo, db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id = crud_dispositivos.get_tambo_id_dispositivo(db, dispositivo_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_dispositivos.update_dispositivo(db, dispositivo_id, dispositivo_data)


@router.put("/dispositivos/{dispositivo_id}/admin-config", response_model=DispositivoAdminRead)
def actualizar_dispositivo_admin(
    dispositivo_id: int,
    dispositivo_data: UpdateDispositivoAdmin, db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)
    
    return crud_dispositivos.update_dispositivo_admin(db, dispositivo_id, dispositivo_data)


@router.put("/dispositivos/{dispositivo_id}/desactivar")
def desactivar_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id = crud_dispositivos.get_tambo_id_dispositivo(db, dispositivo_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_dispositivos.deactivate_dispositivo(db, dispositivo_id)

@router.put("/dispositivos/{dispositivo_id}/recuperar")
def recuperar_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    tambo_id = crud_dispositivos.get_tambo_id_dispositivo(db, dispositivo_id)
    security.es_admin_en_tambo(db, tambo_id, token)

    return crud_dispositivos.activate_dispositivo(db, dispositivo_id)

@router.delete("/dispositivos/{dispositivo_id}", response_model=DispositivoAdminRead)
def eliminar_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security.oauth2_scheme)):
    security.es_superadmin(db, token)

    return crud_dispositivos.delete_dispositivo(db, dispositivo_id)
