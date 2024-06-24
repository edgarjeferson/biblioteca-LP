import sqlite3

def create_tables():
    connection = sqlite3.connect('biblioteca.db')
    cursor = connection.cursor()

    # Crear tabla autores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS autores (
        idautor INTEGER PRIMARY KEY,
        NOMBRES TEXT NOT NULL,
        APELLIDOS TEXT NOT NULL,
        DNI TEXT NOT NULL,
        NACIONALIDAD TEXT NOT NULL
    )
    ''')

    # Crear tabla categorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        idcategoria INTEGER PRIMARY KEY,
        NOMBRE TEXT NOT NULL
    )
    ''')

    # Crear tabla libros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        idlibro INTEGER PRIMARY KEY,
        TITULO TEXT NOT NULL,
        idcategoria INTEGER,
        FOREIGN KEY (idcategoria) REFERENCES categorias(idcategoria)
    )
    ''')

    # Crear tabla libros_autores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros_autores (
        idlibro INTEGER,
        idautor INTEGER,
        PRIMARY KEY (idlibro, idautor),
        FOREIGN KEY (idlibro) REFERENCES libros(idlibro),
        FOREIGN KEY (idautor) REFERENCES autores(idautor)
    )
    ''')

    # Crear tabla prestamos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prestamos (
        idprestamo INTEGER PRIMARY KEY,
        idlibro INTEGER,
        idusuario INTEGER,
        fecha_prestamo TEXT NOT NULL,
        fecha_devolucion TEXT,
        FOREIGN KEY (idlibro) REFERENCES libros(idlibro),
        FOREIGN KEY (idusuario) REFERENCES usuarios(idusuario)
    )
    ''')

    # Crear tabla roles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        idrol INTEGER PRIMARY KEY,
        NOMBRE TEXT NOT NULL
    )
    ''')

    # Crear tabla usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        idusuario INTEGER PRIMARY KEY,
        NOMBRES TEXT NOT NULL,
        APELLIDOS TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        idrol INTEGER,
        FOREIGN KEY (idrol) REFERENCES roles(idrol)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Tablas creadas exitosamente.")
