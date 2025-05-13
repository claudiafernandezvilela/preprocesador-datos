import os
import pandas as pd
import sqlite3
from tabulate import tabulate

def cargar_datos():
    """
    Implementa la funcionalidad de carga de datos desde diferentes fuentes.
    Returns:
        tuple: (datos, ruta, tipo_archivo) donde:
            - datos: DataFrame con los datos cargados o None si hubo error
            - ruta: Ruta del archivo cargado o None
            - tipo_archivo: Tipo de archivo cargado ("CSV", "Excel", "SQLite") o None
    """
    # Mostrar menú de opciones para seleccionar el tipo de archivo
    print("\n===================================")
    print("         Carga de Datos           ")
    print("===================================")
    print("Seleccione el tipo de archivo a cargar:")
    print("  [1] CSV")
    print("  [2] Excel")
    print("  [3] SQLite")
    print("  [4] Volver al menú principal")
    
    # Leer la opción seleccionada por el usuario
    opcion = input("Seleccione una opción: ")
    
    # Si el usuario elige volver al menú principal
    if opcion == "4":
        return None, None, None  # No se carga ningún archivo
    
    # Validar que la opción ingresada sea válida
    if opcion not in ["1", "2", "3"]:
        print("Opción no válida.")
        return None, None, None
    
    # Mapear la opción seleccionada al tipo de archivo correspondiente
    tipo_archivo = {"1": "CSV", "2": "Excel", "3": "SQLite"}[opcion]
    
    try:
        # Llamar a la función correspondiente según el tipo de archivo
        if tipo_archivo == "CSV":
            return cargar_csv()
        elif tipo_archivo == "Excel":
            return cargar_excel()
        elif tipo_archivo == "SQLite":
            return cargar_sqlite()
    except Exception as e:
        # Manejar errores durante la carga de datos
        print(f"Error al cargar los datos: {e}")
        return None, None, None

def cargar_csv():
    """Carga datos desde un archivo CSV."""
    # Solicitar la ruta del archivo CSV al usuario
    ruta = input("Ingrese la ruta del archivo: ")
    # Validar que el archivo exista y tenga la extensión correcta
    if not os.path.exists(ruta) or not ruta.lower().endswith('.csv'):
        print("Error: Archivo no encontrado o no es un archivo CSV válido.")
        return None, None, None
    
    # Cargar los datos del archivo CSV utilizando pandas
    datos = pd.read_csv(ruta)
    
    # Mostrar información básica del dataset cargado
    mostrar_info_dataset(datos, ruta, "CSV")
    
    return datos, ruta, "CSV"

def cargar_excel():
    """Carga datos desde un archivo Excel."""
    # Solicitar la ruta del archivo Excel al usuario
    ruta = input("Ingrese la ruta del archivo: ")
    # Validar que el archivo exista y tenga una extensión válida
    if not os.path.exists(ruta) or not (ruta.lower().endswith('.xlsx') or ruta.lower().endswith('.xls')):
        print("Error: Archivo no encontrado o no es un archivo Excel válido.")
        return None, None, None
        
    # Abrir el archivo Excel para verificar las hojas disponibles
    with pd.ExcelFile(ruta) as xls:
        if len(xls.sheet_names) > 1:
            # Si hay múltiples hojas, mostrar las opciones al usuario
            print("Hojas disponibles:")
            for i, hoja in enumerate(xls.sheet_names, 1):
                print(f"  [{i}] {hoja}")
            # Solicitar al usuario que seleccione una hoja
            opcion_hoja = input("Seleccione una hoja: ")
            try:
                indice = int(opcion_hoja) - 1
                if indice < 0 or indice >= len(xls.sheet_names):
                    raise ValueError
                hoja = xls.sheet_names[indice]
            except ValueError:
                # Si la selección no es válida, usar la primera hoja por defecto
                print("Selección no válida. Usando la primera hoja.")
                hoja = xls.sheet_names[0]
        else:
            # Si solo hay una hoja, seleccionarla automáticamente
            hoja = xls.sheet_names[0]
        
    # Cargar los datos de la hoja seleccionada
    datos = pd.read_excel(ruta, sheet_name=hoja)
    
    # Mostrar información básica del dataset cargado
    mostrar_info_dataset(datos, ruta, "Excel")
    
    return datos, ruta, "Excel"

def cargar_sqlite():
    """Carga datos desde una base de datos SQLite."""
    # Solicitar la ruta de la base de datos SQLite al usuario
    ruta_db = input("Ingrese la ruta de la base de datos SQLite: ")
    # Validar que el archivo exista y tenga una extensión válida
    if not os.path.exists(ruta_db) or not (ruta_db.lower().endswith('.sqlite') or ruta_db.lower().endswith('.db')):
        print("Error: Archivo no encontrado o no es una base de datos SQLite válida.")
        return None, None, None
        
    try:
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        # Obtener la lista de tablas disponibles en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        if not tablas:
            # Si no hay tablas en la base de datos, mostrar un mensaje de error
            print("No se encontraron tablas en la base de datos.")
            conn.close()
            return None, None, None
            
        # Mostrar las tablas disponibles al usuario
        print("Tablas disponibles en la base de datos:")
        for i, (tabla,) in enumerate(tablas, 1):
            print(f"  [{i}] {tabla}")
            
        # Solicitar al usuario que seleccione una tabla
        opcion_tabla = input("Seleccione una tabla: ")
        try:
            indice = int(opcion_tabla) - 1
            if indice < 0 or indice >= len(tablas):
                raise ValueError
            tabla = tablas[indice][0]
        except ValueError:
            # Si la selección no es válida, cerrar la conexión y salir
            print("Selección no válida.")
            conn.close()
            return None, None, None
            
        # Cargar los datos de la tabla seleccionada
        datos = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
        conn.close()
        
        # Mostrar información básica de la tabla cargada
        ruta_completa = f"{ruta_db}|{tabla}"
        mostrar_info_dataset(datos, ruta_completa, "SQLite", tabla_nombre=tabla)
        
        return datos, ruta_completa, "SQLite"
            
    except sqlite3.Error as e:
        # Manejar errores al acceder a la base de datos
        print(f"Error al acceder a la base de datos: {e}")
        return None, None, None

def mostrar_info_dataset(datos, ruta, tipo_archivo, tabla_nombre=None):
    """Muestra información básica sobre el dataset cargado."""
    # Mostrar un mensaje indicando que los datos se cargaron correctamente
    if tabla_nombre:
        print(f'Datos de la tabla "{tabla_nombre}" cargados correctamente.')
    else:
        print("Datos cargados correctamente.")
    
    # Mostrar el número de filas y columnas del dataset
    print(f"Número de filas: {datos.shape[0]}")
    print(f"Número de columnas: {datos.shape[1]}")
    # Mostrar las primeras 5 filas del dataset en formato tabular
    print("Primeras 5 filas:")
    print(tabulate(datos.head(), headers='keys', tablefmt='plain'))
    
    # Mostrar los tipos de datos de cada columna
    print("\nTipos de datos:")
    for columna, tipo in datos.dtypes.items():
        print(f"  {columna}: {tipo}")