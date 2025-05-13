import pandas as pd
import numpy as np
from tabulate import tabulate

def detectar_valores_atipicos(datos, features, target):
    print("\n===================================")
    print("Detección y Manejo de Valores Atípicos")
    print("===================================")

    # Creamos una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Verificar que las columnas en features existan en el dataset
    # (pueden haber sido transformadas por One-Hot Encoding)
    features_existentes = [columna for columna in features if columna in datos_procesados.columns]
    
    # Identificar las columnas numéricas entre las columnas de entrada existentes
    columnas_numericas = []
    for columna in features_existentes:
        if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
            columnas_numericas.append(columna)

    # También incluir las columnas binarias generadas por One-Hot Encoding
    # (obtenemos todas las columnas excepto la target)
    columnas_binarias = []
    for col in datos_procesados.columns:
        if col not in columnas_numericas and col != target:
            # Verificamos si es una columna binaria (contiene solo 0's y 1's)
            if set(datos_procesados[col].dropna().unique()).issubset({0, 1, True, False}):
                columnas_binarias.append(col)

    # Si no hay columnas numéricas, informamos al usuario y no hacemos nada
    if not columnas_numericas and not columnas_binarias:
        print("No se han detectado columnas numéricas ni binarias en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Diccionario para almacenar los valores atípicos encontrados
    valores_atipicos = {}
    hay_val_atipicos = False

    # Detectar valores atípicos en columnas numéricas
    for columna in columnas_numericas:
        Q1 = datos_procesados[columna].quantile(0.25)
        Q3 = datos_procesados[columna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        # Encontrar los valores atípicos
        atipicos = datos_procesados[(datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)]
        
        num_atipicos = len(atipicos)
        if num_atipicos > 0:
            valores_atipicos[columna] = num_atipicos
            hay_val_atipicos = True

    # Detectar valores atípicos en columnas binarias (One-Hot Encoding)
    for columna in columnas_binarias:
        # Determinar los valores válidos según el tipo de columna
        if pd.api.types.is_bool_dtype(datos_procesados[columna]):
            valores_validos = [True, False]
        else:
            valores_validos = [0, 1]
            
        # Las columnas binarias deberían tener solo valores válidos
        atipicos = datos_procesados[~datos_procesados[columna].isin(valores_validos)]
        
        num_atipicos = len(atipicos)
        if num_atipicos > 0:
            valores_atipicos[columna] = num_atipicos
            hay_val_atipicos = True

    # Si no hay valores atípicos, informamos al usuario y no hacemos nada
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

    if opcion == "4":
        print("Operación cancelada.")
        return datos, False
    
    # Validar opción
    if opcion not in ["1", "2", "3"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia elegida
        if opcion == "1":
            filas_iniciales = len(datos_procesados)
            filas_a_eliminar = set()
            for columna in columnas_numericas + columnas_binarias:
                if columna in columnas_numericas:
                    Q1 = datos_procesados[columna].quantile(0.25)
                    Q3 = datos_procesados[columna].quantile(0.75)
                    IQR = Q3 - Q1
                    limite_inferior = Q1 - 1.5 * IQR
                    limite_superior = Q3 + 1.5 * IQR

                    mask_atipicos = (datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)
                else:
                    # Para columnas binarias, determinar valores válidos
                    if pd.api.types.is_bool_dtype(datos_procesados[columna]):
                        valores_validos = [True, False]
                    else:
                        valores_validos = [0, 1]
                    
                    # Identificar valores atípicos (diferentes de los valores válidos)
                    mask_atipicos = ~datos_procesados[columna].isin(valores_validos)

                indices_atipicos = datos_procesados[mask_atipicos].index
                filas_a_eliminar.update(indices_atipicos)

            datos_procesados = datos_procesados.drop(list(filas_a_eliminar))
            filas_finales = len(datos_procesados)

            print(f"\nSe han eliminado {filas_iniciales - filas_finales} filas con valores atípicos.")
        
        elif opcion == "2":
            for columna in columnas_numericas + columnas_binarias:
                if columna in columnas_numericas:
                    Q1 = datos_procesados[columna].quantile(0.25)
                    Q3 = datos_procesados[columna].quantile(0.75)
                    IQR = Q3 - Q1
                    limite_inferior = Q1 - 1.5 * IQR
                    limite_superior = Q3 + 1.5 * IQR
                    mediana = datos_procesados[columna].median()

                    # Corrección: Crear máscaras booleanas separadas y combinarlas con el operador OR
                    mask_inf = datos_procesados[columna] < limite_inferior
                    mask_sup = datos_procesados[columna] > limite_superior
                    mask_combinada = mask_inf | mask_sup
                    
                    # Aplicar el reemplazo usando la máscara combinada
                    datos_procesados.loc[mask_combinada, columna] = mediana
                else:
                    # Para columnas binarias, reemplazar valores atípicos
                    mask_atipicos = ~datos_procesados[columna].isin([0, 1])
                    
                    # Verificar el tipo de datos de la columna y asignar el valor apropiado
                    if pd.api.types.is_bool_dtype(datos_procesados[columna]):
                        # Para columnas booleanas, usar False en lugar de 0
                        datos_procesados.loc[mask_atipicos, columna] = False
                    else:
                        # Para otras columnas numéricas, usar 0
                        mediana = 0  # O usar 1 si prefieres, dependiendo de lo que se ajuste mejor
                        datos_procesados.loc[mask_atipicos, columna] = mediana

            print("\nValores atípicos reemplazados con la mediana de cada columna.")
        
        elif opcion == "3":
            print("\nLos valores atípicos se han mantenido sin cambios.")

        return datos_procesados, True
    
    except Exception as e:
        print(f"Error al manejar los valores atípicos: {e}")
        return datos, False
        