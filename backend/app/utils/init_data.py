from sqlalchemy.orm import Session
from datetime import datetime, time, UTC
from app.models.roles import Rol
from app.models.usuarios import Usuario
from app.models.tambos import Tambo
from app.models.comederos import Comedero
from app.models.usuarios_tambos_roles import UsuarioTamboRol
from app.models.dispositivos import Dispositivo
from app.models.imagenes import Imagen

def insertar_datos_prueba(db: Session):
    # === Insertar roles ===
    if not db.query(Rol).first():
        roles = [
            Rol(nombre="admin", es_admin=True),
            Rol(nombre="usuario", es_admin=False),
            Rol(nombre="Ing. Agrónomo", es_admin=True)
        ]
        db.add_all(roles)
        db.commit()
        print("Roles insertados.")
    #else:
    #    print("Roles ya existen.")

    # === Insertar usuarios ===
    if not db.query(Usuario).first():
        usuarios = [
            Usuario(
                nombres=f"Usuario{i+1}",
                apellidos="Apellido",
                email=f"usuario{i+1}@example.com",
                password="1234",
                fecha_alta=datetime.now(UTC),
                ultimo_acceso=datetime.now(UTC),
                estado=True
            ) for i in range(10)
        ]
        db.add_all(usuarios)
        db.commit()
        print("Usuarios insertados.")
    #else:
    #    print("Usuarios ya existen.")

    # === Insertar tambos ===
    if not db.query(Tambo).first():
        tambos = [
            Tambo(nombre="Tambo Norte", descripcion="Tambo 1", ubicacion="Zona Norte", estado=True),
            Tambo(nombre="Tambo Sur", descripcion="Tambo 2", ubicacion="Zona Sur", estado=True),
            Tambo(nombre="Tambo Este", descripcion="Tambo 3", ubicacion="Zona Este", estado=True),
        ]
        db.add_all(tambos)
        db.commit()
        print("Tambos insertados.")
    #else:
    #    print("Tambos ya existen.")

    # === Asignar usuarios a tambos con roles ===
    if not db.query(UsuarioTamboRol).first():
        asignaciones = [
            UsuarioTamboRol(id_usuario=1, id_tambo=1, id_rol=1),
            UsuarioTamboRol(id_usuario=2, id_tambo=1, id_rol=2),         
            UsuarioTamboRol(id_usuario=2, id_tambo=2, id_rol=3),         
            UsuarioTamboRol(id_usuario=3, id_tambo=2, id_rol=2),
            UsuarioTamboRol(id_usuario=4, id_tambo=2, id_rol=1),
            UsuarioTamboRol(id_usuario=5, id_tambo=3, id_rol=2),
            UsuarioTamboRol(id_usuario=4, id_tambo=3, id_rol=3),
            UsuarioTamboRol(id_usuario=2, id_tambo=3, id_rol=2),
            UsuarioTamboRol(id_usuario=6, id_tambo=3, id_rol=1),
            UsuarioTamboRol(id_usuario=7, id_tambo=3, id_rol=2),
            UsuarioTamboRol(id_usuario=8, id_tambo=3, id_rol=2),
            UsuarioTamboRol(id_usuario=9, id_tambo=3, id_rol=3),
            UsuarioTamboRol(id_usuario=10, id_tambo=3, id_rol=2),
        ]
        db.add_all(asignaciones)
        db.commit()
        print("Asignaciones de usuarios a tambos insertadas.")
    #else:
    #    print("Asignaciones ya existen.")

    # === Insertar comederos ===
    if not db.query(Comedero).first():
        comederos = [
            Comedero(nombre="Comedero A", id_tambo=1, descripcion=None, ubicacion="A1", estado=True),
            Comedero(nombre="Comedero B", id_tambo=2, descripcion=None, ubicacion="B1", estado=True),
            Comedero(nombre="Comedero C", id_tambo=2, descripcion=None, ubicacion="B2", estado=True),
            Comedero(nombre="Comedero D", id_tambo=3, descripcion=None, ubicacion="C1", estado=True),
            Comedero(nombre="Comedero E", id_tambo=3, descripcion=None, ubicacion="C2", estado=True),
            Comedero(nombre="Comedero F", id_tambo=3, descripcion=None, ubicacion="C3", estado=True),
        ]
        db.add_all(comederos)
        db.commit()
        print("Comederos insertados.")
    #else:
    #    print("Comederos ya existen.")

    # === Insertar dispositivos ===
    if not db.query(Dispositivo).first():
        dispositivos = []
        for i in range(3):  # 3 dispositivos en el primer comedero
            dispositivos.append(Dispositivo(
                nombre=f"Dispositivo A{i+1}",
                id_comedero=1,
                usuario_local="pi",
                direccion_local=f"192.168.0.{i+10}",
                puerto_ssh=22,
                usuario_servidor="ubuntu",
                direccion_servidor="servidor.com",
                puerto_servidor=22,
                hora_inicio=time(6, 0),
                hora_fin=time(18, 0),
                intervalo=time(0, 30),
                estado=True
            ))
        for j in range(2, 7):  # un dispositivo para cada uno de los otros comederos (id 2 al 6)
            dispositivos.append(Dispositivo(
                nombre=f"Dispositivo {j}",
                id_comedero=j,
                usuario_local="pi",
                direccion_local=f"192.168.1.{j+10}",
                puerto_ssh=22,
                usuario_servidor="ubuntu",
                direccion_servidor="servidor.com",
                puerto_servidor=22,
                hora_inicio=time(6, 0),
                hora_fin=time(18, 0),
                intervalo=time(0, 30),
                estado=True
            ))
        db.add_all(dispositivos)
        db.commit()
        print("Dispositivos insertados.")
    #else:
    #    print("Dispositivos ya existen.")

    # === Insertar imágenes ===
    if not db.query(Imagen).first():
        dispositivos = db.query(Dispositivo).all()
        imagenes = []
        for dispositivo in dispositivos:
            for i in range(3):
                imagenes.append(Imagen(
                    id_dispositivo=dispositivo.id,
                    path_imagen=f"/imagenes/{dispositivo.nombre}_img{i+1}.jpg",
                    fecha=datetime.now(UTC)
                ))
        db.add_all(imagenes)
        db.commit()
        print("Imágenes insertadas.")
    #else:
    #    print("Imágenes ya existen.")
