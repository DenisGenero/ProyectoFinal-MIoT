import pymysql
import app.config as config

def crear_base_datos():
    conexion = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    cursor = conexion.cursor()
    cursor.execute(
        config.CREATE_DB_CMD
    )
    conexion.close()
    print("Base de datos '" +  (config.DB_NAME) + "' verificada/creada correctamente.")

# Si se ejecuta directamente el archivo
if __name__ == "__main__":
    crear_base_datos()
