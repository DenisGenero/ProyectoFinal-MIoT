# Agro_IoT - API Backend  
---
## Herramientas usadas
- **[FastAPI:](https://fastapi.tiangolo.com/)** Framework web para construir APIs con Python. Permite definir rutas de manera sencilla, validación automática de datos y generación de documentación interactiva.

- **[Uvicorn:](https://www.uvicorn.org/)** ASGI (Asynchronous Server Gateway Interface) que se utiliza para correr aplicaciones FastAPI.

- **[MySQL:](https://dev.mysql.com/doc/)** Sistema de gestión de base de datos relacional. Almacena toda la información estructurada del sistema.

- **[SQLAlchemy:](https://docs.sqlalchemy.org/en/20/)** ORM (Object Relational Mapper) que permite trabajar con la base de datos mediante objetos de Python. Facilita operaciones de consulta, inserción y actualización. Razones para usarlo:

    - Permite mejor organización y mantenimiento del código.
    - Se integra nativamente con FastAPI.
    - Escalable para sistemas más complejos.

- **[PyMySQL:](https://pymysql.readthedocs.io/en/latest/)** Driver que permite a SQLAlchemy conectarse con una base de datos MySQL desde Python.

- **[Pydantic:](https://docs.pydantic.dev/latest/)** Biblioteca para validación de datos mediante modelos. En FastAPI valida automáticamente entrada y salida de datos.

## Base de datos - Modelo relacional  

Se realizó con la herramienta Lucidchart, y se puede acceder a través del siguiente enlace (requiere inicio de sesión): [Agro_IoT DB](https://lucid.app/lucidchart/807cb250-d4ed-495d-998e-6396380c545e/edit?invitationId=inv_fa926f5f-eec0-4fcf-baff-261f1ca83d53)  

## Estructura del proyecto
  
app/  
│  
├── crud/               # Lógica de base de datos con SQLAlchemy  
├── database/        # Conexión a MySQL y definición de modelos ORM  
├── endpoints/      # Rutas de la API  
├── models/           # clases ORM de SQLAlchemy que representan las tablas de la db y sus relaciones.  
├── schemas/         # Modelos Pydantic para validación  
├── utils/                # Script para insertar datos de prueba  
│  
├── \_\_init__.py         # Marca al directorio actual como módulo de Python  
├── main.py            # Archivo principal: arranca el servidor y monta rutas   
│  
requirements.txt       # Dependencias del proyecto

## Comandos utiles  
#### Recomendación:
- **Crear entorno virtual:** python3 -m venv .venv  
- **Activar el entorno virtual (bash):** source ./venv/Scripts/activate  
#### Correr aplicación
- **Instalar dependencias:** pip install -r requirements.txt
- **Levantar el servidor:** uvicorn app.main:app --reload  
  *(--reload: opcional --> reinicia el servidor automáticamente al guardar cambios)*
#### Test de endpoints:
- **Swagger UI:** http://127.0.0.1:8000/docs