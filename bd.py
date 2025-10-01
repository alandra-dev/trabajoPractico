import sqlite3

def crear_bd():
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()

    # Tabla administradores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS administradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasenia TEXT NOT NULL
    )
    """)

    # Tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasenia TEXT NOT NULL
    )
    """)

    # Tabla libros
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        isbn TEXT PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        anio TEXT NOT NULL,
        genero TEXT NOT NULL
    )
    """)

    # Tabla favoritos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favoritos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        isbn_libro TEXT NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(isbn_libro) REFERENCES libros(isbn)
    )
    """)

    conexion.commit()
    conexion.close()

# Ejecutar al iniciar el proyecto
if __name__ == "__main__":
    crear_bd()
