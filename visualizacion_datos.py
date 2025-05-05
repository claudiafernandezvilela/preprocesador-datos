import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler 

def visualizar_datos(datos, features, target):
    """
    Implementa la funcionalidad de visualización de datos.
    
    Args:
        datos: DataFrame con los datos procesados
        features: Lista de nombres de columnas que son variables de entrada
        target: Nombre de la columna objetivo
    
    Returns:
        bool: True si se completó la visualización, False en caso contrario
    """
    print("\n=============================")
    print("Visualización de Datos")
    print("=============================")
    
    # Verificar que el preprocesamiento esté completo
    if datos is None or features is None or target is None:
        print("No es posible visualizar los datos hasta que se complete el preprocesado.")
        print("Por favor, finalice el manejo de valores atípicos antes de continuar.")
        return False
    
    # Verificar que las columnas seleccionadas existen en el DataFrame
    columnas = [columna for columna in features if columna in datos.columns]
    if not columnas:
        print("No se encontraron columnas seleccionadas en los datos.")
        return False
    
    print("\nSeleccione qué tipo de visualización desea generar:")
    print("  [1] Resumen estadístico de las variables seleccionadas")
    print("  [2] Histogramas de variables numéricas")
    print("  [3] Gráficos de dispersión antes y después de la normalización")
    print("  [4] Heatmap de correlación de variables numéricas")
    print("  [5] Volver al menú principal")
    
    try:
        opcion = int(input("\nSeleccione una opción: "))
    except ValueError:
        print("Opción inválida.")
        return False
    
    if opcion == 1:  # Resumen estadísticos
        print("\nResumen estadístico de las variables seleccionadas:")
        print("-------------------------------------------------------------------")
        print("Variable      | Media | Mediana | Desviación Est. | Mínimo | Máximo")
        print("-------------------------------------------------------------------")
        
        # Obtener estadísticas
        estadisticas = datos[columnas].describe().T  # Transpone para tener variables en filas
        
        # Imprimir cada fila
        for variable in estadisticas.index:
            media = round(estadisticas.loc[variable, 'mean'], 1)
            mediana = round(estadisticas.loc[variable, '50%'], 0)
            desv = round(estadisticas.loc[variable, 'std'], 1)
            minimo = round(estadisticas.loc[variable, 'min'], 0)
            maximo = round(estadisticas.loc[variable, 'max'], 0)
            
            print(f"{variable:<13} | {media:<5} | {mediana:<7} | {desv:<15} | {minimo:<6} | {maximo}")
    
    elif opcion == 2:  # Histogramas
        # Filtrar solo columnas numéricas
        cols_numericas = [col for col in columnas if pd.api.types.is_numeric_dtype(datos[col])]
        datos[cols_numericas].hist(bins=20, figsize=(12, 8))
        plt.tight_layout()
        plt.show()
    
    elif opcion == 3:  # Gráficos de dispersión
        for columna in columnas:
            if pd.api.types.is_numeric_dtype(datos[columna]):
                plt.figure(figsize=(6, 4))
                plt.scatter(range(len(datos)), datos[columna], label=f"{columna} (original)", alpha=0.5)
                plt.scatter(range(len(datos)), MinMaxScaler().fit_transform(datos[[columna]]), 
                           label=f"{columna} (normalizado)", alpha=0.5)
                plt.legend()
                plt.title(f"Comparación de {columna} antes y después de la normalización")
                plt.show()
    
    elif opcion == 4:  # Heatmap de correlación
        # Filtrar solo columnas numéricas
        cols_numericas = [col for col in columnas if pd.api.types.is_numeric_dtype(datos[col])]
        plt.figure(figsize=(10, 6))
        sns.heatmap(datos[cols_numericas].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Heatmap de correlación de variables numéricas")
        plt.show()
    
    elif opcion == 5:  # Volver al menú principal
        return True
    
    else:
        print("Opción inválida.")
    
    return True