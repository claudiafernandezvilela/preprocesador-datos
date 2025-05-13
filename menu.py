#!/usr/bin/env python3
import os
from cargar_datos import cargar_datos  
from seleccion_columnas import seleccionar_columnas
from manejo_valores_faltantes import manejo_valores_faltantes
from transformar_datos_categoricos import transformar_datos_categoricos
from normalizado_escalado import normalizar_escalar_datos
from detectar_valores_atipicos import detectar_valores_atipicos
from visualizacion_datos import visualizar_datos
from exportar_datos import exportar_datos

def simbolo(paso_requerido, paso_actual):
    """
    Devuelve un símbolo que representa el estado de un paso en el menú.
    
    Args:
        paso_requerido (float): El paso que se evalúa.
        paso_actual (float): El paso actual del flujo.
    
    Returns:
        str: Símbolo que indica el estado ('✗', '-', '✓').
    """
    if paso_actual < paso_requerido:
        return '✗'  # Paso no disponible
    elif paso_actual == paso_requerido or (paso_requerido == 2 and paso_actual < 3):
        return '-'  # Paso actual
    else:
        return '✓'  # Paso completado

def mostrar_menu(paso, ruta=None, tipo_archivo=None):
    """
    Muestra el menú principal con el estado de cada opción según el paso actual.
    
    Args:
        paso (float): El paso actual del flujo.
        ruta (str): Ruta del archivo cargado (opcional).
        tipo_archivo (str): Tipo de archivo cargado (opcional).
    
    Returns:
        str: Opción seleccionada por el usuario.
    """
    print("\n===================================")
    print("         Menú Principal           ")
    print("===================================")
    
    # Determinar el estado de la carga de datos
    if paso <= 1:
        estado_carga = "ningún archivo cargado"
    else:
        if tipo_archivo == "CSV":
            estado_carga = f"archivo: {os.path.basename(ruta)}"
        elif tipo_archivo == "Excel":
            estado_carga = f"archivo: {os.path.basename(ruta)}"
        elif tipo_archivo == "SQLite":
            partes = ruta.split('|')
            db_path = partes[0]
            tabla = partes[1] if len(partes) > 1 else "desconocida"
            estado_carga = f"tabla: {tabla} de {os.path.basename(db_path)}"
    
    # Mostrar las opciones del menú principal
    print(f"[{simbolo(1, paso)}] 1. Cargar datos ({estado_carga if paso >= 1 else 'ningún archivo cargado'})")
    print(f"[{simbolo(2, paso)}] 2. Preprocesado de datos {'(requiere carga de datos)' if paso < 2 else '(selección de columnas requerida)' if paso == 2 else '(completado)' if paso >= 3 else ''}")
    
    # Mostrar subopciones del preprocesado si el paso es mayor o igual a 2
    if paso >= 2:
        print(f"\t[{simbolo(2.1, paso)}] 2.1 Selección de columnas ({'pendiente' if paso < 2.2 and paso >= 2 else 'completado' if paso > 2.1 else 'requiere carga de datos'})")
        print(f"\t[{simbolo(2.2, paso)}] 2.2 Manejo de valores faltantes ({'pendiente' if paso == 2.2 else 'completado' if paso > 2.2 else 'requiere selección de columnas'})")
        print(f"\t[{simbolo(2.3, paso)}] 2.3 Transformación de datos categóricos ({'pendiente' if paso == 2.3 else 'completado' if paso > 2.3 else 'requiere manejo de valores faltantes'})")
        print(f"\t[{simbolo(2.4, paso)}] 2.4 Normalización y escalado ({'pendiente' if paso == 2.4 else 'completado' if paso > 2.4 else 'requiere transformación categórica'})")
        print(f"\t[{simbolo(2.5, paso)}] 2.5 Detección y manejo de valores atípicos ({'pendiente' if paso == 2.5 else 'completado' if paso > 2.5 else 'requiere normalización'})")
    
    print(f"[{simbolo(3, paso)}] 3. Visualización de datos ({'pendiente' if paso == 3 else 'requiere preprocesado completo' if paso < 3 else 'completado'})")
    print(f"[{simbolo(4, paso)}] 4. Exportar datos ({'pendiente' if paso == 4 else 'requiere visualización de datos' if paso < 4 else 'completado'})")
    print(f"[{simbolo(5, paso) if paso > 4 else '✓' }] 5. Salir ")
    
    # Solicitar la opción seleccionada por el usuario
    return input("\nSeleccione una opción: ")

def mostrar_dialogo_salir():
    """
    Muestra el diálogo de confirmación para salir de la aplicación.
    
    Returns:
        bool: True si el usuario confirma salir, False en caso contrario.
    """
    print("\n===================================")
    print("Salir de la Aplicación")
    print("===================================")
    print("¿Está seguro de que desea salir?")
    print("  [1] Sí")
    print("  [2] No")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        print("Cerrando la aplicación...")
        return True
    else:
        print("Regresando al menú principal...")
        return False

def main():
    """
    Función principal que controla el flujo de la aplicación.
    """
    paso = 1  # Paso inicial
    ruta = None
    tipo_archivo = None
    datos = None
    features = None
    target = None
    
    while True:
        # Mostrar el menú principal y obtener la opción seleccionada
        opcion = mostrar_menu(paso, ruta, tipo_archivo)
        
        if opcion == "1":
            # Cargar datos usando la función importada del módulo cargar_datos
            datos, ruta, tipo_archivo = cargar_datos()
            if datos is not None:
                paso = 2  # Avanzar al paso 2
                features = None  # Resetear selección de columnas
                target = None
  
        elif opcion == "2" and paso >= 2:
            print("Iniciando preprocesado de datos...")
            paso = 2.1  # Avanzar al subpaso 2.1
      
        elif opcion.startswith("2.") and paso >= 2:
            # Opciones de preprocesado
            if opcion == "2.1" and paso >= 2:
                features, target, estado = seleccionar_columnas(datos)
                if estado and features is not None and target is not None:
                    paso = 2.2
            elif opcion == "2.2" and paso >= 2.2:
                datos_procesados, estado = manejo_valores_faltantes(datos, features, target)
                if estado:
                    datos = datos_procesados
                    paso = 2.3
            elif opcion == "2.3" and paso >= 2.3:
                datos_procesados, estado = transformar_datos_categoricos(datos, features, target)
                if estado:
                    datos = datos_procesados
                    paso = 2.4
            elif opcion == "2.4" and paso >= 2.4:
                datos_procesados, estado = normalizar_escalar_datos(datos, features, target)
                if estado:
                    datos = datos_procesados
                    paso = 2.5
            elif opcion == "2.5" and paso >= 2.5:
                datos_procesados, estado = detectar_valores_atipicos(datos, features, target)
                if estado:
                    datos = datos_procesados
                    paso = 3
                    
        elif opcion == "3" and paso >= 3:
            estado_visualizacion = visualizar_datos(datos, features, target)
            if estado_visualizacion:
                paso = 4
        elif opcion == "4" and paso >= 4:
            estado_exportacion = exportar_datos(datos, features, target)
            if estado_exportacion:
                paso = 5
        elif opcion == "5":
            if mostrar_dialogo_salir():
                break
        else:
            print("Opción no válida o no disponible en este momento.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupción por el usuario.")
    finally:
        print("Programa finalizado.")
