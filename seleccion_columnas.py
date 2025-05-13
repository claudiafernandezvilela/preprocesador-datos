import pandas as pd
from tabulate import tabulate

def seleccionar_columnas(datos):
    """
    Permite al usuario seleccionar las columnas de entrada (features) y la columna de salida (target) 
    de un conjunto de datos.

    Args:
        datos (DataFrame): Dataset original.

    Returns:
        tuple: (features, target, bool) donde:
            - features: Lista de nombres de las columnas seleccionadas como entrada.
            - target: Nombre de la columna seleccionada como salida.
            - bool: True si la selección fue exitosa, False en caso contrario.
    """
    print("\n===================================")
    print("         Selección de Columnas    ")
    print("===================================")

    # Mostrar todas las columnas disponibles en el dataset
    print("Columnas disponibles en los datos:  ")
    for i, columna in enumerate(datos.columns, 1):
        print(f"  [{i}] {columna}")

    # Selección de las columnas de entrada (features)
    while True:
        try:
            entrada_features = input("\nIngrese los números de las columnas de entrada (features), separados por comas:")
            
            # Comprobar si el usuario quiere cancelar la operación
            if entrada_features == str(len(datos.columns) + 1):
                print("Operación cancelada.")
                return None, None, False
            
            # Convertir la entrada del usuario en una lista de índices
            indices_features = [int(idx.strip()) for idx in entrada_features.split(",")]
            
            # Validar que los índices estén dentro del rango de columnas disponibles
            if any(idx <= 0 or idx > len(datos.columns) for idx in indices_features):
                print("Error: Uno o más índices fuera de rango.")
                continue
                
            # Obtener los nombres de las columnas seleccionadas como features
            features = [datos.columns[idx - 1] for idx in indices_features]
            break  # Salir del bucle si la selección es válida
            
        except ValueError:
            # Manejar errores si el usuario ingresa valores no numéricos
            print("Error: Ingrese números válidos separados por comas.")
    
    # Selección de la columna de salida (target)
    while True:
        try:
            entrada_target = input("\nIngrese el número de la columna de salida (target): ")

            # Comprobar si el usuario quiere cancelar la operación
            if entrada_target == str(len(datos.columns) + 1):
                print("Operación cancelada.")
                return None, None, False
            
            # Convertir la entrada del usuario en un índice
            indice_target = int(entrada_target.strip())

            # Validar que el índice esté dentro del rango de columnas disponibles
            if indice_target <= 0 or indice_target > len(datos.columns):
                print("Error: Índice fuera de rango.")
                continue

            # Obtener el nombre de la columna seleccionada como target
            target = datos.columns[indice_target - 1]
            
            # Comprobar que el target no esté incluido en las features seleccionadas
            if target in features or not features:
                print(" ⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")
                continue

            break  # Salir del bucle si la selección es válida

        except ValueError:
            # Manejar errores si el usuario ingresa valores no numéricos
            print("Error: Ingrese un número válido.")

    # Mostrar la selección guardada al usuario
    print("\nSelección guardada:")
    print(f"Features = {features}")
    print(f"Target = {target}")

    # Retornar las columnas seleccionadas y el estado de éxito
    return features, target, True





    