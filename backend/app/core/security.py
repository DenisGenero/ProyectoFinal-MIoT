from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import app.config as config
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.models.usuarios_tambos_roles import UsuarioTamboRol
from app.models.roles import Rol
from app.models.dispositivos import Dispositivo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
oauth2_scheme_device = HTTPBearer()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(config.UY_TZ) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def decode_token(token: str, secret: str = config.SECRET_KEY , algorithm: str =[config.ALGORITHM]):
    try:
        payload = jwt.decode(token, secret, algorithm)
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
        
    return payload


def get_usuario_from_token(
        db: Session,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
        ) -> Usuario:
    if type(token) is str:
        payload = decode_token(token)
    else:
        payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return usuario


def es_superadmin(
        db: Session,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
        ) -> bool:
    current_user = get_usuario_from_token(db, token)
    if not current_user.es_superadmin:
        raise HTTPException(status_code=403, detail="No tiene permisos de administrador")
    
    return True


def ususario_pertenece_tambo(
        db: Session,
        tambo_id: int,
        user: Usuario) -> bool:
    
    pertenece = db.query(UsuarioTamboRol).filter(
        UsuarioTamboRol.id_usuario == user.id,
        UsuarioTamboRol.id_tambo == tambo_id
    ).first()
    if not pertenece:
        raise HTTPException(status_code=403, detail="No pertenece al tambo")
    if not pertenece.estado:
        raise HTTPException(status_code=403, detail="Pertenencia en el tambo desactivada")
    
    return True

def es_admin_en_tambo(
        db: Session,
        tambo_id: int,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
        ) -> bool:
    current_user = get_usuario_from_token(db, token)
    
    ususario_pertenece_tambo(db, tambo_id, current_user)
    
    # ¿Tiene rol admin en ese tambo?
    rol = db.query(Rol).join(UsuarioTamboRol, UsuarioTamboRol.id_rol == Rol.id).filter(
        UsuarioTamboRol.id_usuario == current_user.id,
        UsuarioTamboRol.id_tambo == tambo_id,
    ).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if not rol.es_admin:
        raise HTTPException(status_code=403, detail="No tiene permisos de administrador en este tambo")
    
    return True
'''
def decode_mac_from_token(token: str):
    try:
        payload = jwt.decode(
            token,
            config.SECRET_DISPOSITIVOS,
            algorithms=[config.ALGORITHM]
        )
        mac = payload.get("mac")
        if not mac:
            raise HTTPException(status_code=401, detail="Token inválido: falta MAC")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return mac
'''

def get_dispositivo_from_jwt(
        db: Session,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme_device)
    ):
    payload = decode_token(token.credentials, config.SECRET_DISPOSITIVOS)
    mac = payload.get("mac")
    dispositivo = db.query(Dispositivo).filter(Dispositivo.mac_address == mac).first()
    if not dispositivo:
        raise HTTPException(status_code=401, detail="Dispositivo no encontrado")
    if not dispositivo.estado:
        raise HTTPException(status_code=401, detail="Dispositivo inactivo")

    return dispositivo

"""
def get_dispositivo_from_token(
        db: Session,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme_device)):
    api_key = token.credentials
    dispositivo = db.query(Dispositivo).filter(Dispositivo.api_key == api_key).first()
    if not dispositivo:
        raise HTTPException(status_code=401, detail="Token inválido")
    if not dispositivo.estado:
        raise HTTPException(status_code=401, detail="Dispositivo inactivo")
    
    return dispositivo
    """
