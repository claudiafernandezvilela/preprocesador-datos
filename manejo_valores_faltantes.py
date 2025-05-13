import pandas as pd
import numpy as np
from tabulate import tabulate

def manejo_valores_faltantes(datos, features, target):
    print("\n===================================")
    print("   Manejo de Valores Faltantes")
    print("===================================")

    # Creamos una copia del dataset para no modificar el original

    datos_procesados = datos.copy(deep=True)

    # Obtenemos todas las columnas seleccionadas
    columnas_seleccionadas = features + [target]

    # Comprobar si hay valores faltantes en las columnas seleccionadas
    valores_faltantes = {}
    hay_val_faltantes = False

    for columna in columnas_seleccionadas:
        nulos = datos_procesados[columna].isna().sum()
        if nulos > 0:
            valores_faltantes[columna] = nulos
            hay_val_faltantes = True

    # Si no hay valores faltantes, informamos al usuario y no hacemos nada
    if not hay_val_faltantes:
        print("No se han detectado valores faltantes en las columnas seleccionadas.")
        print("No es necesario aplicar ninguna estrategia. ")
        return datos_procesados, True
    
    # Mostrar los valores faltantes encontrados
    print("Se han detectado valores faltantes en las siguientes columnas seleccionadas:")
    for columna, cantidad in valores_faltantes.items():
        print(f"  - {columna}: {cantidad} valores faltantes")

    # Menú para manejar los valores faltantes
    print("\nSelecciones una estrategia para manejar los valores faltantes:")
    print("  [1] Eliminar filas con valores faltantes")
    print("  [2] Rellenar con la media de la columna")
    print("  [3] Rellenar con la mediana de la columna")
    print("  [4] Rellenar con la moda de la columna")
    print("  [5] Rellenar con un valor constante")
    print("  [6] Volver al menú principal")

    opcion = input("Seleccione una opción: ")

    if opcion == "6":
        print("Operación cancelada.")
        return datos, False
    
    # Validar opción
    if opcion not in ["1", "2", "3", "4", "5"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia elegida
        if opcion == "1":
            filas_iniciales = len(datos_procesados)
            datos_procesados = datos_procesados.dropna(subset=columnas_seleccionadas)
            filas_finales = len(datos_procesados)
            print(f"\nSe han eliminado {filas_iniciales - filas_finales} filas con valores faltantes.")
        
        elif opcion == "2":
            for columna in columnas_seleccionadas:
                if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
                    media = datos_procesados[columna].mean()
                    datos_procesados[columna] = datos_procesados[columna].fillna(media)
                else:
                    print(f"La columna '{columna}' no es numérica. No se pueden rellenar con la media.")
            print("\nValores faltantes rellenados con la media de cada columna numérica.")
        
        elif opcion == "3":
            for columna in columnas_seleccionadas:
                if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
                    mediana = datos_procesados[columna].median()
                    datos_procesados[columna] = datos_procesados[columna].fillna(mediana)
                else:
                    print(f"La columna '{columna}' no es numérica. No se pueden rellenar con la mediana.")
            print("\nValores faltantes rellenados con la mediana de cada columna numérica.")
        
        elif opcion == "4":
            for columna in columnas_seleccionadas:
                moda = datos_procesados[columna].mode()[0]  # La moda puede ser múltiple, tomamos la primera
                datos_procesados[columna] = datos_procesados[columna].fillna(moda)
            print("\nValores faltantes rellenados con la moda de cada columna.")

        elif opcion == "5":
            try:
                valor_constante = float(input("Seleccione un valor numérico para reemplazar los valores faltantes: "))
                for columna in columnas_seleccionadas:
                    datos_procesados[columna] = datos_procesados[columna].fillna(valor_constante)
                print("\nValores faltantes rellenados con el valor constante.")
            except ValueError:
                print("Error: Debe ingresar un valor numérico válido.")
                return datos, False
        

        return datos_procesados, True
            
    except Exception as e:
        print(f"Error al manejar los valores faltantes: {e}")
        return datos, False

    return datos, False
    

