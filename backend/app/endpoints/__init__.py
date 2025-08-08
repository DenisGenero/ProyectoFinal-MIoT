# app/endpoints/__init__.py

from fastapi import APIRouter
from app.endpoints import usuarios, roles, tambos, usuarios_tambos, comederos, dispositivos, imagenes

router = APIRouter()
router.include_router(usuarios.router, prefix="/api", tags=["Usuarios"])
router.include_router(roles.router, prefix="/api", tags=["Roles"])
router.include_router(tambos.router, prefix="/api", tags=["Tambos"])
router.include_router(usuarios_tambos.router, prefix="/api", tags=["Usuarios-Tambos"])
router.include_router(comederos.router, prefix="/api", tags=["Comederos"])
router.include_router(dispositivos.router, prefix="/api", tags=["Dispositivos"])
router.include_router(imagenes.router, prefix="/api", tags=["Imágenes"])