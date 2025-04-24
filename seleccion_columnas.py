import pandas as pd
from tabulate import tabulate

def seleccionar_columnas(datos):
    print("\n===================================")
    print("         Selección de Columnas    ")
    print("===================================")

    # Mostrar todas las columnas disponibles
    print("Columnas disponibles en los datos:  ")
    for i, columna in enumerate(datos.columns, 1):
        print(f"  [{i}] {columna}")
    
    # Selección de las columnas de entrada (features)
    while True:
        try:
            entrada_features = input("\nIngrese los números de las columnas de entrada (features), separados por comas:")

            # Comprobar si el usuario quiere volver al menú principal
            if entrada_features == str(len(datos.columns) + 1):
                print("Operación cancelada.")
                return None, None, False
            
            # Convertir la entrada a una lista de índices
            indices_features = [int(idx.strip()) for idx in entrada_features.split(",")]

            # Validar los índices
            if any(idx <= 0 or idx > len(datos.columns) for idx in indices_features):
                print("Error: Uno o más índices fuera de rango.")
                continue

            # Obtener los nombres de las columnas
            features = [datos.columns[idx - 1] for idx in indices_features]
            break

        except ValueError:
            print("Error: Ingrese números válidos separados por comas.")

    # Selección de la columna de salida (target)
    while True:
        try:
            entrada_target = input("\nIngrese el número de la columna de salida (target): ")

            # Comprobar si el usuario quiere volver al menú principal
            if entrada_target == str(len(datos.columns) + 1):
                print("Operación cancelada.")
                return None, None, False
            
            # Convertir la entrada a un índice
            indice_target = int(entrada_target.strip())

            # Validar el índice
            if indice_target <= 0 or indice_target > len(datos.columns):
                print("Error: Índice fuera de rango.")
                continue

            # Obtener el nombre de la columna
            target = datos.columns[indice_target - 1]
            
            # Comprobar que el target no esté en features
            if target in features or not features:
                print(" ⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")
                continue

            break

        except ValueError:
            print("Error: Ingrese un número válido.")

    # Mostrar la selección guardada
    print("\nSelección guardada:")
    print(f"Features = {features}")
    print(f"Target = {target}")

    return features, target, True

def mostrar_seleccion_actual(features, target):
    if features and target:
        print("\nSelección actual:")
        print(f"Features: {', '.join(features)}")
        print(f"Target: {target}")
    
    else:
        print("\nNo hay selección de columnas realizada. ")



    