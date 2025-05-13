import pandas as pd
import numpy as np
from tabulate import tabulate

def detectar_valores_atipicos(datos, features, target):
    """
    Detecta y maneja valores atípicos en un conjunto de datos.
    
    Args:
        datos (DataFrame): Dataset original.
        features (list): Lista de columnas de entrada a analizar.
        target (str): Nombre de la columna objetivo (target).
    
    Returns:
        tuple: (datos_procesados, bool) donde:
            - datos_procesados: DataFrame con los datos procesados.
            - bool: True si se procesaron los datos correctamente, False en caso contrario.
    """
    print("\n===================================")
    print("Detección y Manejo de Valores Atípicos")
    print("===================================")

    # Crear una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Verificar que las columnas en features existan en el dataset
    # Esto es útil si las columnas fueron transformadas (por ejemplo, con One-Hot Encoding)
    features_existentes = [columna for columna in features if columna in datos_procesados.columns]
    
    # Identificar las columnas numéricas entre las columnas de entrada existentes
    columnas_numericas = []
    for columna in features_existentes:
        if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
            columnas_numericas.append(columna)

    # Identificar columnas binarias generadas por One-Hot Encoding
    # Excluimos la columna objetivo (target)
    columnas_binarias = []
    for col in datos_procesados.columns:
        if col not in columnas_numericas and col != target:
            # Verificar si la columna es binaria (contiene solo 0's y 1's)
            if set(datos_procesados[col].dropna().unique()).issubset({0, 1, True, False}):
                columnas_binarias.append(col)

    # Si no hay columnas numéricas ni binarias, no es necesario aplicar estrategias
    if not columnas_numericas and not columnas_binarias:
        print("No se han detectado columnas numéricas ni binarias en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Diccionario para almacenar los valores atípicos encontrados
    valores_atipicos = {}
    hay_val_atipicos = False

    # Detectar valores atípicos en columnas numéricas
    for columna in columnas_numericas:
        # Calcular el rango intercuartílico (IQR) para identificar valores atípicos
        Q1 = datos_procesados[columna].quantile(0.25)
        Q3 = datos_procesados[columna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        # Identificar valores fuera de los límites
        atipicos = datos_procesados[(datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)]
        
        # Si se encuentran valores atípicos, almacenarlos
        num_atipicos = len(atipicos)
        if num_atipicos > 0:
            valores_atipicos[columna] = num_atipicos
            hay_val_atipicos = True

    # Detectar valores atípicos en columnas binarias
    for columna in columnas_binarias:
        # Determinar los valores válidos según el tipo de columna
        if pd.api.types.is_bool_dtype(datos_procesados[columna]):
            valores_validos = [True, False]
        else:
            valores_validos = [0, 1]
            
        # Identificar valores que no sean válidos
        atipicos = datos_procesados[~datos_procesados[columna].isin(valores_validos)]
        
        # Si se encuentran valores atípicos, almacenarlos
        num_atipicos = len(atipicos)
        if num_atipicos > 0:
            valores_atipicos[columna] = num_atipicos
            hay_val_atipicos = True

    # Si no se detectan valores atípicos, informar al usuario
    if not hay_val_atipicos:
        print("No se han detectado valores atípicos en las columnas seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Mostrar los valores atípicos encontrados
    print("Se han detectado valores atípicos en las siguientes columnas:")
    for columna, cantidad in valores_atipicos.items():
        print(f"  - {columna}: {cantidad} valores atípicos detectados")

    # Menú para manejar valores atípicos
    print("\nSeleccione una estrategia para manejar los valores atípicos:")
    print("  [1] Eliminar filas con valores atípicos")
    print("  [2] Reemplazar valores atípicos con la mediana de la columna")
    print("  [3] Mantener valores atípicos sin cambios")
    print("  [4] Volver al menú principal")

    opcion = input("Seleccione una opción: ")

    # Si el usuario elige volver al menú principal
    if opcion == "4":
        print("Operación cancelada.")
        return datos, False
    
    # Validar la opción seleccionada
    if opcion not in ["1", "2", "3"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia seleccionada
        if opcion == "1":
            # Eliminar filas con valores atípicos
            filas_iniciales = len(datos_procesados)
            filas_a_eliminar = set()
            for columna in columnas_numericas + columnas_binarias:
                if columna in columnas_numericas:
                    # Calcular límites para valores atípicos
                    Q1 = datos_procesados[columna].quantile(0.25)
                    Q3 = datos_procesados[columna].quantile(0.75)
                    IQR = Q3 - Q1
                    limite_inferior = Q1 - 1.5 * IQR
                    limite_superior = Q3 + 1.5 * IQR

                    # Identificar índices de filas con valores atípicos
                    mask_atipicos = (datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)
                else:
                    # Para columnas binarias, identificar valores no válidos
                    if pd.api.types.is_bool_dtype(datos_procesados[columna]):
                        valores_validos = [True, False]
                    else:
                        valores_validos = [0, 1]
                    mask_atipicos = ~datos_procesados[columna].isin(valores_validos)

                indices_atipicos = datos_procesados[mask_atipicos].index
                filas_a_eliminar.update(indices_atipicos)

            # Eliminar las filas identificadas
            datos_procesados = datos_procesados.drop(list(filas_a_eliminar))
            filas_finales = len(datos_procesados)

            print(f"\nSe han eliminado {filas_iniciales - filas_finales} filas con valores atípicos.")
        
        elif opcion == "2":
            # Reemplazar valores atípicos con la mediana
            for columna in columnas_numericas + columnas_binarias:
                if columna in columnas_numericas:
                    # Calcular límites y mediana
                    Q1 = datos_procesados[columna].quantile(0.25)
                    Q3 = datos_procesados[columna].quantile(0.75)
                    IQR = Q3 - Q1
                    limite_inferior = Q1 - 1.5 * IQR
                    limite_superior = Q3 + 1.5 * IQR
                    mediana = datos_procesados[columna].median()

                    # Reemplazar valores atípicos con la mediana
                    mask_combinada = (datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)
                    datos_procesados.loc[mask_combinada, columna] = mediana
                else:
                    # Para columnas binarias, reemplazar valores no válidos
                    mask_atipicos = ~datos_procesados[columna].isin([0, 1])
                    if pd.api.types.is_bool_dtype(datos_procesados[columna]):
                        datos_procesados.loc[mask_atipicos, columna] = False
                    else:
                        datos_procesados.loc[mask_atipicos, columna] = 0

            print("\nValores atípicos reemplazados con la mediana de cada columna.")
        
        elif opcion == "3":
            # Mantener valores atípicos sin cambios
            print("\nLos valores atípicos se han mantenido sin cambios.")

        return datos_procesados, True
    
    except Exception as e:
        # Manejar errores durante el procesamiento
        print(f"Error al manejar los valores atípicos: {e}")
        return datos, False