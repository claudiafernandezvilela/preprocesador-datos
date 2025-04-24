import pandas as pd
import numpy as np
from tabulate import tabulate

def detectar_valores_atipicos(datos, features, target):
    print("\n===================================")
    print("         Detección y Manejo de Valores Atípicos")
    print("===================================")

    # Creamos una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Identificar las columnas numéricas entre las columnas de entrada seleccionadas
    columnas_numericas = []
    for columna in features:
        if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
            columnas_numericas.append(columna)

    # Si no hay columnas numéricas, informamos al usuario y no hacemos nada
    if not columnas_numericas:
        print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Diccionario para almacenar los valores atípicos encontrados
    valores_atipicos = {}
    hay_val_atipicos = False

     # Detectar valores atípicos usando el método del rango intercuartílico (IQR)
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
    
    # Si no hay valores atípicos, informamos al usuario y no hacemos nada
    if not hay_val_atipicos:
        print("No se han detectado valores atípicos en las columnas numéricas seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Mostrar los valores atípicos encontrados
    print("Se han detectado valores atípicos en las siguientes columnas numéricas seleccionadas:")
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
            for columna in columnas_numericas:
                Q1 = datos_procesados[columna].quantile(0.25)
                Q3 = datos_procesados[columna].quantile(0.75)
                IQR = Q3 - Q1
                limite_inferior = Q1 - 1.5 * IQR
                limite_superior = Q3 + 1.5 * IQR

                mask_atipicos = (datos_procesados[columna] < limite_inferior) | (datos_procesados[columna] > limite_superior)
                indices_atipicos = datos_procesados[mask_atipicos].index

                filas_a_eliminar.update(indices_atipicos)

            datos_procesados = datos_procesados.drop(list(filas_a_eliminar))
            filas_finales = len(datos_procesados)

            print(f"\nSe han eliminado {filas_iniciales - filas_finales} filas con valores atípicos.")
        
        elif opcion == "2":
            for columna in columnas_numericas:
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

            print("\nValores atípicos reemplazados con la mediana de cada columna.")
        
        elif opcion == "3":
            print("\nLos valores atípicos se han mantenido sin cambios.")

        return datos_procesados, True
    
    except Exception as e:
        print(f"Error al manejar los valores atípicos: {e}")
        return datos, False
        