import os
import pandas as pd
from tabulate import tabulate

def exportar_datos(datos, features, target):
    """
    Implementa la funcionalidad de exportación de datos después del preprocesamiento.
    
    Args:
        datos: DataFrame con los datos procesados.
        features: Lista de nombres de columnas que son variables de entrada.
        target: Nombre de la columna objetivo.
    
    Returns:
        bool: True si se completó la exportación, False en caso contrario.
    """
    print("\n===================================")
    print("         Exportación de Datos           ")
    print("===================================")
    
    # Verificar que el preprocesamiento y la visualización estén completos
    if datos is None or features is None or target is None:
        print("No es posible exportar los datos hasta que se complete el preprocesado y la visualización.")
        print("Por favor, finalice todas las etapas antes de continuar.")
        return False
    
    # Preparar los datos para la exportación (crear una copia para evitar modificar los originales)
    datos_a_exportar = datos.copy()
    
    # Verificar que todas las columnas en features + target existen en datos_a_exportar
    todas_columnas = features.copy()
    if target not in todas_columnas:
        todas_columnas.append(target)  # Agregar la columna objetivo si no está incluida
    
    # Verificar si las columnas necesarias están presentes en los datos procesados
    for columna in todas_columnas:
        if columna not in datos_a_exportar.columns:
            print(f"Advertencia: La columna '{columna}' no se encuentra en los datos procesados.")
    
    # Mostrar una vista previa de los datos a exportar
    print("\nDatos a exportar (primeras 5 filas):")
    try:
        # Intentar mostrar solo las columnas relevantes (features + target)
        columnas_existentes = [col for col in todas_columnas if col in datos_a_exportar.columns]
        if columnas_existentes:
            print(tabulate(datos_a_exportar[columnas_existentes].head(), headers='keys', tablefmt='plain'))
        else:
            # Si no hay columnas relevantes, mostrar todo el DataFrame
            print(tabulate(datos_a_exportar.head(), headers='keys', tablefmt='plain'))
    except Exception as e:
        # Manejar errores al mostrar la vista previa
        print(f"Error al mostrar la vista previa de los datos: {e}")
        print("Mostrando estructura básica:")
        print(f"Forma del DataFrame: {datos_a_exportar.shape}")
        print(f"Columnas disponibles: {', '.join(datos_a_exportar.columns.tolist())}")
    
    # Mostrar información general sobre los datos
    print(f"Total de filas: {datos_a_exportar.shape[0]}, Total de columnas: {datos_a_exportar.shape[1]}")
    
    # Mostrar opciones de formato de exportación
    print("Seleccione el formato de exportación:")
    print("  [1] CSV (.csv)")
    print("  [2] Excel (.xlsx)")
    print("  [3] Volver al menú principal")
    
    try:
        # Leer la opción seleccionada por el usuario
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        # Manejar errores si el usuario ingresa un valor no numérico
        print("Opción inválida.")
        return False
    
    if opcion == 3:  # Volver al menú principal
        return False
    
    if opcion not in [1, 2]:  # Validar que la opción sea válida
        print("Opción inválida.")
        return False
    
    # Solicitar nombre del archivo de salida (sin extensión)
    nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
    
    if not nombre_archivo:  # Validar que el nombre del archivo no esté vacío
        print("Nombre de archivo no válido.")
        return False
    
    # Exportar según el formato seleccionado
    try:
        if opcion == 1:  # Exportar como CSV
            ruta_completa = f"{nombre_archivo}.csv"
            datos_a_exportar.to_csv(ruta_completa, index=False)
            print(f'Datos exportados correctamente como "{ruta_completa}".')
        elif opcion == 2:  # Exportar como Excel
            ruta_completa = f"{nombre_archivo}.xlsx"
            datos_a_exportar.to_excel(ruta_completa, index=False)
            print(f'Datos exportados correctamente como "{ruta_completa}".')
        
        return True  # Exportación completada con éxito
        
    except Exception as e:
        # Manejar errores durante la exportación
        print(f"Error al exportar los datos: {e}")
        return False