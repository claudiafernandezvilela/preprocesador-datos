import os

def simbolo(paso_requerido, paso_actual):
    if paso_actual < paso_requerido:
        return '✗'
    elif paso_actual == paso_requerido or (paso_requerido == 2 and paso_actual < 3):
        return '-'
    else:
        return '✓'

def mostrar_menu(paso, ruta):
    print("\n=============================")
    print(" Menú Principal ")
    print("=============================")

    print(f"[{simbolo(1, paso)}] 1. Cargar datos ({'ningún archivo cargado' if paso <= 1 else f'archivo {os.path.basename(ruta)} cargado'})")
    print(f"[{simbolo(2, paso)}] 2. Preprocesado de datos {'(requiere carga de datos)' if paso < 2 else '(completado)' if paso >= 3 else '(en progreso)'}")
    
    # Subopciones siempre visibles
    print(f"\t[{simbolo(2.1, paso)}] 2.1 Selección de columnas ({'pendiente' if paso < 2.2 and paso >= 2.1 else 'completado' if paso > 2.1 else 'requiere carga de datos'})")
    print(f"\t[{simbolo(2.2, paso)}] 2.2 Manejo de valores faltantes ({'pendiente' if paso == 2.2 else 'completado' if paso > 2.2 else 'requiere selección de columnas'})")
    print(f"\t[{simbolo(2.3, paso)}] 2.3 Transformación de datos categóricos ({'pendiente' if paso == 2.3 else 'completado' if paso > 2.3 else 'requiere manejo de valores faltantes'})")
    print(f"\t[{simbolo(2.4, paso)}] 2.4 Normalización y escalado ({'pendiente' if paso == 2.4 else 'completado' if paso > 2.4 else 'requiere transformación categórica'})")
    print(f"\t[{simbolo(2.5, paso)}] 2.5 Detección y manejo de valores atípicos ({'pendiente' if paso == 2.5 else 'completado' if paso > 2.5 else 'requiere normalización'})")
    
    print(f"[{simbolo(3, paso)}] 3. Visualización de datos ({'pendiente' if paso == 3 else 'requiere preprocesado completo' if paso < 3 else 'completado'})")
    print(f"[{simbolo(4, paso)}] 4. Exportar datos ({'pendiente' if paso == 4 else 'requiere visualización de datos' if paso < 4 else 'completado'})")
    
    print("[✓] 5. Salir")
    
    return input("\nSeleccione una opción: ")

def mostrar_dialogo_salir():
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
    paso = 1
    ruta = None
    while True:
        opcion = mostrar_menu(paso, ruta)
        if opcion == "1" and paso <= 1:
            print("Cargando datos...")
            ruta = "datos.csv"
            paso = 2
        elif opcion == "2.1" and paso == 2:
            print("Seleccionando columnas...")
            paso = 2.2
        elif opcion == "2.2" and paso == 2.2:
            print("Manejando valores faltantes...")
            paso = 2.3
        elif opcion == "2.3" and paso == 2.3:
            print("Transformando datos categóricos...")
            paso = 2.4
        elif opcion == "2.4" and paso == 2.4:
            print("Normalizando datos...")
            paso = 2.5
        elif opcion == "2.5" and paso == 2.5:
            print("Detectando valores atípicos...")
            paso = 3
        elif opcion == "3" and paso == 3:
            print("Visualizando datos...")
            paso = 4
        elif opcion == "4" and paso == 4:
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

