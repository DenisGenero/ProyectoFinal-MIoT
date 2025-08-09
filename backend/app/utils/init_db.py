import pymysql

def crear_base_datos():
    """Crea la base de datos agro_iot si no existe."""
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conexion.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS agro_iot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    conexion.close()
    print("Base de datos 'agro_iot' verificada/creada correctamente.")

# Si se ejecuta directamente el archivo
if __name__ == "__main__":
    crear_base_datos()
