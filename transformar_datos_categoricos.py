import pandas as pd
import numpy as np
from tabulate import tabulate

def transformar_datos_categoricos(datos, features, target):
    """
    Transforma las columnas categóricas de un conjunto de datos utilizando diferentes estrategias.

    Args:
        datos (DataFrame): Dataset original.
        features (list): Lista de columnas de entrada seleccionadas.
        target (str): Nombre de la columna objetivo.

    Returns:
        tuple: (datos_procesados, bool) donde:
            - datos_procesados: DataFrame con los datos transformados.
            - bool: True si la transformación fue exitosa, False en caso contrario.
    """
    print("\n===================================")
    print(" Transformación de Datos Categóricos")
    print("===================================")

    # Crear una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Obtener todas las columnas de entrada seleccionadas
    columnas_seleccionadas = features.copy()

    # Identificar columnas categóricas en las columnas seleccionadas
    columnas_categoricas = []
    for columna in columnas_seleccionadas:
        # Verificar si la columna es de tipo objeto o categórico
        if pd.api.types.is_object_dtype(datos_procesados[columna]) or isinstance(datos_procesados[columna].dtype, pd.CategoricalDtype):
            columnas_categoricas.append(columna)

    # Si no hay columnas categóricas, informar al usuario y salir
    if not columnas_categoricas:
        print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna transformación.")
        return datos_procesados, True

    # Mostrar las columnas categóricas encontradas
    print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
    for columna in columnas_categoricas:
        print(f"  - {columna}")

    # Mostrar menú de estrategias de transformación
    print("\nSeleccione una estrategia de transformación: ")
    print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
    print("  [2] Label Encoding (convierte categorías a números enteros)")
    print("  [3] Volver al menú principal")

    # Leer la opción seleccionada por el usuario
    opcion = input("Seleccione una opción: ")

    # Si el usuario elige volver al menú principal
    if opcion == "3":
        print("Operación cancelada.")
        return datos, False
    
    # Validar que la opción seleccionada sea válida
    if opcion not in ["1", "2"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia seleccionada
        if opcion == "1":
            # One-Hot Encoding
            for columna in columnas_categoricas:
                # Generar columnas binarias para cada categoría
                dummies = pd.get_dummies(datos_procesados[columna], prefix=columna, drop_first=False)
                # Concatenar las nuevas columnas al DataFrame original
                datos_procesados = pd.concat([datos_procesados, dummies], axis=1)
                # Eliminar la columna original
                datos_procesados = datos_procesados.drop(columna, axis=1)

            print("\nTransformación completada con One-Hot Encoding.")

        elif opcion == "2":
            # Label Encoding
            for columna in columnas_categoricas:
                # Obtener valores únicos (excluyendo NaN)
                valores_unicos = [valor for valor in datos_procesados[columna].unique() if pd.notna(valor)]
                valores_unicos.sort()  # Ordenar para obtener un mapeo consistente
                
                # Crear un diccionario de mapeo (valor_original -> índice numérico)
                mapeo = {valor: i for i, valor in enumerate(valores_unicos)}
                
                # Aplicar el mapeo a la columna
                datos_procesados[columna] = datos_procesados[columna].map(mapeo)

            print("\nTransformación completada con Label Encoding.")
        
        return datos_procesados, True  # Retornar el DataFrame transformado y éxito
    
    except Exception as e:
        # Manejar errores durante la transformación
        print(f"Error al transformar los datos categóricos: {e}")
        return datos, False