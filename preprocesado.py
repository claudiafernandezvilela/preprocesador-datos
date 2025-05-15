import pandas as pd
from tabulate import tabulate
import numpy as np

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

def manejo_valores_faltantes(datos, features, target):
    """
    Maneja los valores faltantes en un conjunto de datos aplicando diferentes estrategias.
    
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
    print("   Manejo de Valores Faltantes")
    print("===================================")

    # Crear una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Obtenemos todas las columnas seleccionadas (features + target)
    columnas_seleccionadas = features + [target]

    # Comprobar si hay valores faltantes en las columnas seleccionadas
    valores_faltantes = {}
    hay_val_faltantes = False

    for columna in columnas_seleccionadas:
        # Contar valores nulos en cada columna
        nulos = datos_procesados[columna].isna().sum()
        if nulos > 0:
            valores_faltantes[columna] = nulos
            hay_val_faltantes = True

    # Si no hay valores faltantes, informar al usuario y salir
    if not hay_val_faltantes:
        print("No se han detectado valores faltantes en las columnas seleccionadas.")
        print("No es necesario aplicar ninguna estrategia.")
        return datos_procesados, True
    
    # Mostrar los valores faltantes encontrados
    print("Se han detectado valores faltantes en las siguientes columnas seleccionadas:")
    for columna, cantidad in valores_faltantes.items():
        print(f"  - {columna}: {cantidad} valores faltantes")

    # Menú para manejar los valores faltantes
    print("\nSeleccione una estrategia para manejar los valores faltantes:")
    print("  [1] Eliminar filas con valores faltantes")
    print("  [2] Rellenar con la media de la columna")
    print("  [3] Rellenar con la mediana de la columna")
    print("  [4] Rellenar con la moda de la columna")
    print("  [5] Rellenar con un valor constante")
    print("  [6] Volver al menú principal")

    # Leer la opción seleccionada por el usuario
    opcion = input("Seleccione una opción: ")

    # Si el usuario elige volver al menú principal
    if opcion == "6":
        print("Operación cancelada.")
        return datos, False
    
    # Validar que la opción seleccionada sea válida
    if opcion not in ["1", "2", "3", "4", "5"]:
        print("Opción no válida.")
        return datos, False
    
    try:
        # Aplicar la estrategia elegida
        if opcion == "1":
            # Eliminar filas con valores faltantes
            filas_iniciales = len(datos_procesados)
            datos_procesados = datos_procesados.dropna(subset=columnas_seleccionadas)
            filas_finales = len(datos_procesados)
            print(f"\nSe han eliminado {filas_iniciales - filas_finales} filas con valores faltantes.")
        
        elif opcion == "2":
            # Rellenar valores faltantes con la media de cada columna numérica
            for columna in columnas_seleccionadas:
                if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
                    media = datos_procesados[columna].mean()
                    datos_procesados[columna] = datos_procesados[columna].fillna(media)
                else:
                    print(f"La columna '{columna}' no es numérica. No se pueden rellenar con la media.")
            print("\nValores faltantes rellenados con la media de cada columna numérica.")
        
        elif opcion == "3":
            # Rellenar valores faltantes con la mediana de cada columna numérica
            for columna in columnas_seleccionadas:
                if pd.api.types.is_numeric_dtype(datos_procesados[columna]):
                    mediana = datos_procesados[columna].median()
                    datos_procesados[columna] = datos_procesados[columna].fillna(mediana)
                else:
                    print(f"La columna '{columna}' no es numérica. No se pueden rellenar con la mediana.")
            print("\nValores faltantes rellenados con la mediana de cada columna numérica.")
        
        elif opcion == "4":
            # Rellenar valores faltantes con la moda de cada columna
            for columna in columnas_seleccionadas:
                moda = datos_procesados[columna].mode()[0]  # La moda puede ser múltiple, tomamos la primera
                datos_procesados[columna] = datos_procesados[columna].fillna(moda)
            print("\nValores faltantes rellenados con la moda de cada columna.")

        elif opcion == "5":
            # Rellenar valores faltantes con un valor constante proporcionado por el usuario
            try:
                valor_constante = float(input("Seleccione un valor numérico para reemplazar los valores faltantes: "))
                for columna in columnas_seleccionadas:
                    datos_procesados[columna] = datos_procesados[columna].fillna(valor_constante)
                print("\nValores faltantes rellenados con el valor constante.")
            except ValueError:
                print("Error: Debe ingresar un valor numérico válido.")
                return datos, False

        return datos_procesados, True  # Retornar el DataFrame procesado y éxito
        
    except Exception as e:
        # Manejar errores durante el procesamiento
        print(f"Error al manejar los valores faltantes: {e}")
        return datos, False

def transformar_datos_categoricos(datos, features, target):
    """
    Transforma las columnas categóricas de un conjunto de datos utilizando diferentes estrategias.

    Args:
        datos (DataFrame): Dataset original.
        features (list): Lista de columnas de entrada seleccionadas.
        target (str): Nombre de la columna objetivo.

    Returns:
        tuple: (datos_procesados, bool) donde:
            - datos_procesados: DataFrame con los datos transformados.
            - bool: True si la transformación fue exitosa, False en caso contrario.
    """
    print("\n===================================")
    print(" Transformación de Datos Categóricos")
    print("===================================")

    # Crear una copia del dataset para no modificar el original
    datos_procesados = datos.copy(deep=True)

    # Obtener todas las columnas de entrada seleccionadas
    columnas_seleccionadas = features.copy()

    # Identificar columnas categóricas en las columnas seleccionadas
    columnas_categoricas = []
    for columna in columnas_seleccionadas:
        # Verificar si la columna es de tipo objeto o categórico
        if pd.api.types.is_object_dtype(datos_procesados[columna]) or isinstance(datos_procesados[columna].dtype, pd.CategoricalDtype):
            columnas_categoricas.append(columna)

    # Si no hay columnas categóricas, informar al usuario y salir
    if not columnas_categoricas:
        print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
        print("No es necesario aplicar ninguna transformación.")
        return datos_procesados, True

    # Mostrar las columnas categóricas encontradas
    print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
    for columna in columnas_categoricas:
        print(f"  - {columna}")

    # Mostrar menú de estrategias de transformación
    print("\nSeleccione una estrategia de transformación: ")
    print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
    print("  [2] Label Encoding (convierte categorías a números enteros)")
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
        # Aplicar la estrategia seleccionada
        if opcion == "1":
            # One-Hot Encoding
            for columna in columnas_categoricas:
                # Generar columnas binarias para cada categoría
                dummies = pd.get_dummies(datos_procesados[columna], prefix=columna, drop_first=False)
                # Concatenar las nuevas columnas al DataFrame original
                datos_procesados = pd.concat([datos_procesados, dummies], axis=1)
                # Eliminar la columna original
                datos_procesados = datos_procesados.drop(columna, axis=1)

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
                datos_procesados[columna] = datos_procesados[columna].map(mapeo)

            print("\nTransformación completada con Label Encoding.")
        
        return datos_procesados, True  # Retornar el DataFrame transformado y éxito
    
    except Exception as e:
        # Manejar errores durante la transformación
        print(f"Error al transformar los datos categóricos: {e}")
        return datos, False

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
    