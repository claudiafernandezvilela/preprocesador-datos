import pandas as pd
import numpy as np
from tabulate import tabulate

def transformar_datos_categoricos(datos, features, target):
    print("\n===================================")
    print("         Transformación de Datos Categóricos")
    print("===================================")

    # Creamos una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Obtenemos todas las columnas de entrada seleccionadas
    columnas_seleccionadas = features.copy()

    # Comprobar si hay columnas categóricas en las columnas seleccionadas
    columnas_categoricas = []
    for columna in columnas_seleccionadas:
        if pd.api.types.is_object_dtype(datos_procesados[columna]) or pd.api.types.is_categorical_dtype(datos_procesados[columna]):
            columnas_categoricas.append(columna)

    # Si no hay columnas categóricas, informamos al usuario y no hacemos nada
    if not columnas_categoricas:
        print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna transformación.")
        return datos_procesados, True

    # Mostrar las columnas categóricas encontradas
    print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
    for columna in columnas_categoricas:
        print(f"  - {columna}")

    # Menú de las estrategias de transformación
    print("\nSeleccione una estrategia de transformación: ")
    print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
    print("  [2] Label Encoding (convierte categorías a números enteros)")
    print("  [3] Volver al menú principal")

    opcion = input("Seleccione una opción: ")

    if opcion == "3":
        print("Operación cancelada.")
        return datos, False
    
    # Validar opción
    if opcion not in ["1", "2"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia elegida
        if opcion == "1":
            # One-Hot Encoding
            for columna in columnas_categoricas:
                # Aplicar One-Hot Encoding
                dummies = pd.get_dummies(datos_procesados[columna], prefix=columna, drop_first=False)
                # Concatenar las nuevas columnas al DataFrame original
                datos_procesados = pd.concat([datos_procesados, dummies], axis=1)
                # Eliminar la columna original
                datos_procesados.drop(columna, axis=1)

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
                # Primero crear una copia para no modificar la columna mientras iteramos
                nuevo_valores = datos_procesados[columna].copy()
                
                # Aplicar el mapeo manteniendo los NaN como NaN
                for i, valor in enumerate(datos_procesados[columna]):
                    if pd.notna(valor):
                        nuevo_valores.iloc[i] = mapeo[valor]
                
                # Actualizar la columna en el DataFrame
                datos_procesados[columna] = nuevo_valores

            print("\nTransformación completada con Label Encoding.")
        
        return datos_procesados, True
    
    except Exception as e:
        print(f"Error al transformar los datos categóricos: {e}")
        return datos, False