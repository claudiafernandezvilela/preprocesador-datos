import pandas as pd
import numpy as np
from tabulate import tabulate

def normalizar_escalar_datos(datos, features, target):
    print("\n===================================")
    print("         Normalización y Escalado")
    print("===================================")

    # Creamos una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Identificar las colunmnas númericas entre las columnas de entrada seleccionadas
    columnas_numericas = []
    for columna in features:
        if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
            columnas_numericas.append(columna)

    # Si no hay columnas numéricas, informamos al usuario y no hacemos nada
    if not columnas_numericas:
        print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna normalización.")
        return datos_procesados, True
    
    # Mostrar las columnas numéricas encontradas
    print("Se han detectado columnas numéricas en las variables de entrada seleccionadas: ")
    for columna in columnas_numericas:
        print(f"  - {columna}")

    # Menú de las estrategias de normalización
    print("\nSeleccione una estrategia de normalización: ")
    print("  [1] Min-Max Scaling (escala valores entre 0 y 1)")
    print("  [2] Z-score Normalization (media 0, desviación estándar 1)")
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
            # Min-Max Scaling
            for columna in columnas_numericas:
                min_val = datos_procesados[columna].min()
                max_val = datos_procesados[columna].max()
                
                # Evitar división por cero si min_val == max_val
                if min_val == max_val:
                    datos_procesados[columna] = 0  # Si todos los valores son iguales, se normalizan a 0
                    print(f"Columna '{columna}': Todos los valores son iguales ({min_val}). Normalizados a 0.")
                else:
                    datos_procesados[columna] = (datos_procesados[columna] - min_val) / (max_val - min_val)
                #    print(f"Columna '{columna}': Normalizada con Min-Max Scaling (min={min_val:.4f}, max={max_val:.4f})")
            
            print("\nNormalización completada con Min-Max Scaling.")
        
        elif opcion == "2":
            # Z-score Normalization
            for columna in columnas_numericas:
                media = datos_procesados[columna].mean()
                desv = datos_procesados[columna].std()
                
                if desv == 0:
                    datos_procesados[columna] = 0
                    print(f"Columna '{columna}': No hay variación (std=0). Todos normalizados a 0.")
                else:
                    datos_procesados[columna] = (datos_procesados[columna] - media) / desv
                #    print(f"Columna '{columna}': Normalizada con Z-score (media={media:.4f}, std={desv:.4f})")
            
            print("\nNormalización completada con Z-score Normalization.")

        return datos_procesados, True
    
    except Exception as e:
        print(f"Error al normalizar los datos: {e}")
        return datos, False