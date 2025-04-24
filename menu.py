import os
from cargar_datos import cargar_datos  
from seleccion_columnas import seleccionar_columnas, mostrar_seleccion_actual

def simbolo(paso_requerido, paso_actual):
    if paso_actual < paso_requerido:
        return '✗'
    elif paso_actual == paso_requerido or (paso_requerido == 2 and paso_actual < 3):
        return '-'
    else:
        return '✓'

def mostrar_menu(paso, ruta=None, tipo_archivo=None, features=None, target=None):
    """
    Muestra el menú principal con el estado de cada opción según el paso actual.
    """
    print("\n===================================")
    print("         Menú Principal           ")
    print("===================================")
    
    # Estado de carga de datos
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
    
    print(f"[{simbolo(1, paso)}] 1. Cargar datos ({estado_carga if paso >= 1 else 'ningún archivo cargado'})")
    print(f"[{simbolo(2, paso)}] 2. Preprocesado de datos {'(requiere carga de datos)' if paso < 2 else '(selección de columnas requerida)' if paso == 2 else '(completado)' if paso >= 3 else ''}")
    
    # Mostrar subopciones solo si estamos en o después del paso 2
    if paso >= 2:
        print(f"\t[{simbolo(2.1, paso)}] 2.1 Selección de columnas ({'pendiente' if paso < 2.2 and paso >= 2 else 'completado' if paso > 2.1 else 'requiere carga de datos'})")
        print(f"\t[{simbolo(2.2, paso)}] 2.2 Manejo de valores faltantes ({'pendiente' if paso == 2.2 else 'completado' if paso > 2.2 else 'requiere selección de columnas'})")
        print(f"\t[{simbolo(2.3, paso)}] 2.3 Transformación de datos categóricos ({'pendiente' if paso == 2.3 else 'completado' if paso > 2.3 else 'requiere manejo de valores faltantes'})")
        print(f"\t[{simbolo(2.4, paso)}] 2.4 Normalización y escalado ({'pendiente' if paso == 2.4 else 'completado' if paso > 2.4 else 'requiere transformación categórica'})")
        print(f"\t[{simbolo(2.5, paso)}] 2.5 Detección y manejo de valores atípicos ({'pendiente' if paso == 2.5 else 'completado' if paso > 2.5 else 'requiere normalización'})")
    
    print(f"[{simbolo(3, paso)}] 3. Visualización de datos ({'pendiente' if paso == 3 else 'requiere preprocesado completo' if paso < 3 else 'completado'})")
    print(f"[{simbolo(4, paso)}] 4. Exportar datos ({'pendiente' if paso == 4 else 'requiere visualización de datos' if paso < 4 else 'completado'})")
    print("[✓] 5. Salir")
    
    return input("\nSeleccione una opción: ")

def mostrar_dialogo_salir():
    """
    Muestra el diálogo de confirmación para salir de la aplicación.
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
    paso = 1
    ruta = None
    tipo_archivo = None
    datos = None
    features = None
    target = None
    
    while True:
        opcion = mostrar_menu(paso, ruta, tipo_archivo, features, target)
        
        if opcion == "1":
            # Cargar datos usando la función importada del módulo cargar_datos
            datos, ruta, tipo_archivo = cargar_datos()
            if datos is not None:
                paso = 2
                # Resetear selección de columnas si se cargan nuevos datos
                features = None
                target = None
        elif opcion == "2" and paso >= 2:
            # Menú de preprocesado
            print("\n===================================")
            print("         Preprocesado de Datos    ")
            print("===================================")
            print("Seleccione una opción de preprocesado:")
            print("  [1] Selección de columnas")
            if paso >= 2.2:
                print("  [2] Manejo de valores faltantes")
            if paso >= 2.3:
                print("  [3] Transformación de datos categóricos")
            if paso >= 2.4:
                print("  [4] Normalización y escalado")
            if paso >= 2.5:
                print("  [5] Detección y manejo de valores atípicos")
            print("  [0] Volver al menú principal")
            
            subopcion = input("\nSeleccione una opción: ")
            
            if subopcion == "1":
                # Selección de columnas
                features, target, estado = seleccionar_columnas(datos)
                if estado and features is not None and target is not None:
                    paso = 2.2  # Avanzar al siguiente paso
            elif subopcion == "2" and paso >= 2.2:
                print("Manejando valores faltantes...")
                paso = 2.3
            elif subopcion == "3" and paso >= 2.3:
                print("Transformando datos categóricos...")
                paso = 2.4
            elif subopcion == "4" and paso >= 2.4:
                print("Normalizando datos...")
                paso = 2.5
            elif subopcion == "5" and paso >= 2.5:
                print("Detectando valores atípicos...")
                paso = 3
            elif subopcion == "0":
                # Volver al menú principal
                continue
            else:
                print("Opción no válida o no disponible en este momento.")
        elif opcion.startswith("2.") and paso >= 2:
            # Opciones directas de preprocesado
            if opcion == "2.1" and paso >= 2:
                # Selección de columnas
                features, target, estado = seleccionar_columnas(datos)
                if estado and features is not None and target is not None:
                    paso = 2.2  # Avanzar al siguiente paso
            elif opcion == "2.2" and paso >= 2.2:
                print("Manejando valores faltantes...")
                paso = 2.3
            elif opcion == "2.3" and paso >= 2.3:
                print("Transformando datos categóricos...")
                paso = 2.4
            elif opcion == "2.4" and paso >= 2.4:
                print("Normalizando datos...")
                paso = 2.5
            elif opcion == "2.5" and paso >= 2.5:
                print("Detectando valores atípicos...")
                paso = 3
        elif opcion == "3" and paso >= 3:
            print("Visualizando datos...")
            paso = 4
        elif opcion == "4" and paso >= 4:
            print("Exportando datos...")
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

