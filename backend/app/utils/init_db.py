import pymysql
import app.config as config
import os

def crear_base_datos():
    try:
        conexion = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
    except Exception:
        print("Error: Iniciar el motor de la DB")
        os._exit(1)
    cursor = conexion.cursor()
    cursor.execute(
        config.CREATE_DB_CMD
    )
    conexion.close()
    print("Base de datos '" +  (config.DB_NAME) + "' verificada/creada correctamente.")

# Si se ejecuta directamente el archivo
if __name__ == "__main__":
    crear_base_datos()
