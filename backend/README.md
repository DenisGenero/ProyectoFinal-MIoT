# Agro_IoT - API Backend - FastAPI + MySQL
---
## Herramientas usadas
- **FastAPI:** Framework web para construir APIs con Python. Permite definir rutas de manera sencilla, validación automática de datos y generación de documentación interactiva.

- **Uvicorn:** ASGI (Asynchronous Server Gateway Interface) que se utiliza para correr aplicaciones FastAPI.

- **MySQL:** Sistema de gestión de base de datos relacional. Almacena toda la información estructurada del sistema.

- **SQLAlchemy:** ORM (Object Relational Mapper) que permite trabajar con la base de datos mediante objetos de Python. Facilita operaciones de consulta, inserción y actualización. Razones para usarlo:

    - Permite mejor organización y mantenimiento del código.
    - Se integra nativamente con FastAPI.
    - Escalable para sistemas más complejos.

- **PyMySQL:** Driver que permite a SQLAlchemy conectarse con una base de datos MySQL desde Python.

- **Pydantic:** Biblioteca para validación de datos mediante modelos. En FastAPI valida automáticamente entrada y salida de datos.

## Estructura del proyecto
  
app/  
│  
├── crud/               # Lógica de base de datos con SQLAlchemy  
├── database/        # Conexión a MySQL y definición de modelos ORM  
├── endpoints/      # Rutas de la API  
├── models/           # clases ORM de SQLAlchemy que representan las tablas de la db y sus relaciones.  
├── schemas/          # Modelos Pydantic para validación  
│  
├── main.py            # Archivo principal: arranca el servidor y monta rutas  
├── \_\_init__.py         # Marca el paquete como módulo de Python  
│  
requirements.txt       # Dependencias del proyecto

## Comandos útiles
- **Instalar dependencias:** pip install -r requirements.txt
- **Levantar el servidor:** uvicorn app.main:app --reload  
  *(--reload: reinicia el servidor automáticamente al guardar cambios)*