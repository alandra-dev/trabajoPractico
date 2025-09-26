import sqlite3

# Administradores
def agregar_administrador(usuario, contrasenia): #ingresa un nuevo administrador
    conexion = sqlite3.connect("biblioteca.db") 
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO administradores (usuario, contrasenia) VALUES (?, ?)", (usuario, contrasenia))
        conexion.commit() 
        return True # se registró con éxito
    except sqlite3.IntegrityError:
        return False # Usuario ya existe
    finally:
        conexion.close()

def verificar_admin(usuario, contrasenia):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor() # 
    cursor.execute("SELECT * FROM administradores WHERE usuario=? AND contrasenia=?", (usuario, contrasenia))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None # Retorna True si encontró coincidencia

#  Usuarios 
def agregar_usuario(usuario, contrasenia): # ingresa un nuevo usuario
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, contrasenia) VALUES (?, ?)", (usuario, contrasenia))
        conexion.commit() 
        return True # se registró con éxito
    except sqlite3.IntegrityError: # Usuario ya existe
        return False # Usuario ya existe
    finally:
        conexion.close()

# Verificar usuario
def verificar_usuario(usuario, contrasenia):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasenia=?", (usuario, contrasenia))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None # Retorna True si encontró coincidencia

# Libros 
def agregar_libro(isbn, titulo, autor, anio, genero):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO libros VALUES (?, ?, ?, ?, ?)", (isbn, titulo, autor, anio, genero))
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()

def modificar_libro(isbn, titulo, autor, anio, genero):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE libros SET titulo=?, autor=?, anio=?, genero=? WHERE isbn=?", (titulo, autor, anio, genero, isbn))
    conexion.commit()
    modificado = cursor.rowcount > 0 # Verifica si se modificó algún registro
    conexion.close()
    return modificado

def eliminar_libro(isbn):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE isbn=?", (isbn,))
    conexion.commit()
    borrado = cursor.rowcount > 0
    conexion.close()
    return borrado

def obtener_libros(filtro=None):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    if filtro:
        cursor.execute("""
            SELECT * FROM libros
            WHERE titulo LIKE ? AND autor LIKE ? AND genero LIKE ? AND isbn LIKE ? AND anio LIKE ?
        """, (f"%{filtro.get('titulo','')}%",
              f"%{filtro.get('autor','')}%",
              f"%{filtro.get('genero','')}%",
              f"%{filtro.get('isbn','')}%",
              f"%{filtro.get('anio','')}%"))
    else:
        cursor.execute("SELECT * FROM libros")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

#  Favoritos 
def agregar_favorito(usuario_id, isbn_libro):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM favoritos WHERE usuario_id=? AND isbn_libro=?", (usuario_id, isbn_libro))
    if cursor.fetchone():
        conexion.close()
        return False  # Ya existe
    cursor.execute("INSERT INTO favoritos(usuario_id, isbn_libro) VALUES (?, ?)", (usuario_id, isbn_libro))
    conexion.commit()
    conexion.close()
    return True

def obtener_favoritos(usuario_id):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT libros.* FROM libros 
        JOIN favoritos ON libros.isbn = favoritos.isbn_libro
        WHERE favoritos.usuario_id=?
    """, (usuario_id,)) 
    resultados = cursor.fetchall()
    conexion.close()
    return resultados
def eliminar_favorito(usuario_id, isbn_libro):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM favoritos WHERE usuario_id=? AND isbn_libro=?", (usuario_id, isbn_libro))
    conexion.commit()
    eliminado = cursor.rowcount > 0
    conexion.close()
    return eliminado