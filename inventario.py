import sqlite3

#Funcion para crear base de datos y la tabla productos
def crear_base_datos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')

    conexion.commit()
    conexion.close()

#Funcion para agregar un nuevo producto, pidiendo al usuario que complete los campos que se van mostrando en pantalla
def registrar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese una breve descripción del producto: ")
    cantidad = int(input("Ingrese la cantidad disponible del producto: "))
    precio = float(input("Ingrese el precio del producto: "))
    categoria = input("Ingrese la categoría del producto: ")

    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio": precio,
        "categoria": categoria
    }

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (:nombre, :descripcion, :cantidad, :precio, :categoria)
    ''', producto)

    conexion.commit()
    conexion.close()

    print("Producto registrado.")

#Funcion que muestra todos los productos que se encuentran ingresados en la base de datos
def mostrar_productos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        print("\nInventario:")
        print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
        print("----------------------------------------------------------------------")
        for producto in productos:
            producto_diccionario = {
                "id": producto[0],
                "nombre": producto[1],
                "descripcion": producto[2],
                "cantidad": producto[3],
                "precio": producto[4],
                "categoria": producto[5]
            }
            print(f"{producto_diccionario['id']} | {producto_diccionario['nombre']} | {producto_diccionario['descripcion']} | {producto_diccionario['cantidad']} | {producto_diccionario['precio']} | {producto_diccionario['categoria']}")
    else:
        print("No hay productos ingresados.")

    conexion.close()

#Funcion que indicandole un Id de producto me da la opcion de modificar su cantidad
def actualizar_producto():
    id_producto = int(input("Ingrese el ID del producto que desea actualizar: "))
    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("UPDATE productos SET cantidad = :cantidad WHERE id = :id", {"cantidad": nueva_cantidad, "id": id_producto})

    if cursor.rowcount > 0:
        print("Cantidad actualizada.")
    else:
        print("No se encontró un producto con ese ID.")

    conexion.commit()
    conexion.close()

#Funcion que dandole el Id de producto lo elimina de la base de datos
def eliminar_producto():
    id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = :id", {"id": id_producto})

    if cursor.rowcount > 0:
        print("Producto eliminado.")
    else:
        print("No se encontró un producto con ese ID.")

    conexion.commit()
    conexion.close()

#Funcion que indicandole Id , nombre o categoria del producto lo devuelve si existe
def buscar_producto():
    filtro = input("Ingrese el ID, nombre o categoría del producto que desea buscar: ")

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    if filtro.isdigit():
        cursor.execute("SELECT * FROM productos WHERE id = :id", {"id": int(filtro)})
    else:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE :criterio OR categoria LIKE :criterio", {"criterio": f"%{filtro}%"})

    productos = cursor.fetchall()

    if productos:
        print("\nResultados de la búsqueda:")
        print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
        print("----------------------------------------------------------------------")
        for producto in productos:
            producto_dict = {
                "id": producto[0],
                "nombre": producto[1],
                "descripcion": producto[2],
                "cantidad": producto[3],
                "precio": producto[4],
                "categoria": producto[5]
            }
            print(f"{producto_dict['id']} | {producto_dict['nombre']} | {producto_dict['descripcion']} | {producto_dict['cantidad']} | {producto_dict['precio']} | {producto_dict['categoria']}")
    else:
        print("No se encontraron productos que coincidan la búsqueda solicitada.")

    conexion.close()

#Funcion que indicandole un limite de cantidad, me indica que productos estan en esa cantidad o por debajo
def reporte_bajo_stock():
    limite = int(input("Ingrese el límite de cantidad para el reporte de bajo stock: "))

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad <= :limite", {"limite": limite})
    productos = cursor.fetchall()

    if productos:
        print("\nProductos con bajo stock:")
        print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
        print("-" * 60)
        for producto in productos:
            producto_dict = {
                "id": producto[0],
                "nombre": producto[1],
                "descripcion": producto[2],
                "cantidad": producto[3],
                "precio": producto[4],
                "categoria": producto[5]
            }
            print(f"{producto_dict['id']} | {producto_dict['nombre']} | {producto_dict['descripcion']} | {producto_dict['cantidad']} | {producto_dict['precio']} | {producto_dict['categoria']}")
    else:
        print("No hay productos con bajo stock según el límite indicado.")

    conexion.close()

def main():
    crear_base_datos()

#Menu del programa, donde cada opcion elegida por el usuario llama a su funcion correspondiente
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Generar reporte de bajo stock")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

if __name__ == "__main__":
    main()
