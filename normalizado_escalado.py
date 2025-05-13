import pandas as pd
import numpy as np
from tabulate import tabulate

def normalizar_escalar_datos(datos, features, target):
    """
    Aplica estrategias de normalización y escalado a las columnas numéricas de un conjunto de datos.

    Args:
        datos (DataFrame): Dataset original.
        features (list): Lista de columnas de entrada a analizar.
        target (str): Nombre de la columna objetivo.

    Returns:
        tuple: (datos_procesados, bool) donde:
            - datos_procesados: DataFrame con los datos procesados.
            - bool: True si se procesaron los datos correctamente, False en caso contrario.
    """
    print("\n===================================")
    print("Normalización y Escalado")
    print("===================================")

    # Crear una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Identificar las columnas numéricas entre las columnas de entrada seleccionadas
    columnas_numericas = []
    columnas_que_existen = [columna for columna in features if columna in datos_procesados.columns]
    
    for columna in columnas_que_existen:
        if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
            columnas_numericas.append(columna)

    # Si no hay columnas numéricas, informar al usuario y salir
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
        # Aplicar la estrategia elegida
        if opcion == "1":
            # Min-Max Scaling
            for columna in columnas_numericas:
                min_val = datos_procesados[columna].min()
                max_val = datos_procesados[columna].max()
                
                # Evitar división por cero si todos los valores son iguales
                if min_val == max_val:
                    datos_procesados[columna] = 0  # Normalizar a 0 si no hay variación
                    print(f"Columna '{columna}': Todos los valores son iguales ({min_val}). Normalizados a 0.")
                else:
                    datos_procesados[columna] = (datos_procesados[columna] - min_val) / (max_val - min_val)
            
            print("\nNormalización completada con Min-Max Scaling.")
        
        elif opcion == "2":
            # Z-score Normalization
            for columna in columnas_numericas:
                media = datos_procesados[columna].mean()
                desv = datos_procesados[columna].std()
                
                # Evitar división por cero si no hay variación
                if desv == 0:
                    datos_procesados[columna] = 0
                    print(f"Columna '{columna}': No hay variación (std=0). Todos normalizados a 0.")
                else:
                    datos_procesados[columna] = (datos_procesados[columna] - media) / desv
            
            print("\nNormalización completada con Z-score Normalization.")

        return datos_procesados, True  # Retornar el DataFrame procesado y éxito
    
    except Exception as e:
        # Manejar errores durante el procesamiento
        print(f"Error al normalizar los datos: {e}")
        return datos, False