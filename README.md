# Pipeline de Preprocesamiento de Datos

Este proyecto consistirá en el desarrollo de una aplicación Python que guía el preprocesamiento de datos a través de una interfaz interactiva en la línea de comandos siguiendo buenas prácticas de ingeniería de software.

## Descripción

Esta aplicación implementa un pipeline completo de preprocesamiento de datos con una interfaz de línea de comandos (CLI) que guía al usuario a través de todas las etapas necesarias para preparar un conjunto de datos para análisis o modelado. El sistema está diseñado con un enfoque modular y sigue un flujo estructurado que garantiza la correcta secuencia de operaciones.

## Características

- **Carga de datos** desde múltiples fuentes (CSV, Excel, SQLite)
- **Preprocesamiento estructurado**:
  - Selección de columnas (features y target)
  - Manejo de valores faltantes
  - Transformación de datos categóricos
  - Normalización y escalado
  - Detección y manejo de valores atípicos
- **Visualización de datos** con gráficos informativos
- **Exportación de datos** procesados en diferentes formatos
- **Interfaz de usuario intuitiva** con indicadores de progreso

## Requisitos

- Python 3.6 o superior
- Dependencias (instalables vía pip):
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - tabulate
  - sqlite3 (incluido en la biblioteca estándar de Python)

## Instalación del programa

1. Clonar este repositorio:
   ```
   git clone https://github.com/tu-usuario/pipeline-preprocesamiento.git
   cd pipeline-preprocesamiento
   ```

2. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución del programa

1. Ejecutar la aplicación:
   ```
   python menu.py
   ```

2. Seguir las instrucciones en pantalla para avanzar por las diferentes etapas del pipeline.

### Flujo de trabajo típico

1. **Cargar datos** desde un archivo CSV, Excel o base de datos SQLite
2. **Seleccionar columnas** de interés para el análisis
3. **Manejar valores faltantes** mediante diferentes estrategias
4. **Transformar datos categóricos** a formato numérico
5. **Normalizar y escalar** las variables numéricas
6. **Detectar y manejar valores atípicos**
7. **Visualizar los datos** procesados con diferentes gráficos
8. **Exportar los datos** procesados a un nuevo archivo

## Pruebas unitarias

El proyecto incluye pruebas unitarias exhaustivas para garantizar el correcto funcionamiento de todos los módulos. Incluye un archivo de pruebas para comprobar la buena ejecución tanto del menú, otro para toda la parte del preprocesado de datos y, otro archivo que se asegura del funcionamiento de la carga, visualizacón y exportación de los datos. Ejemplo de ejecución de alguna de las pruebas:

```
python test_menu.py
```

## Ejemplos de uso

### Cargar un archivo CSV

```
===================================
         Menú Principal           
===================================
[-] 1. Cargar datos (ningún archivo cargado)
[✗] 2. Preprocesado de datos (requiere carga de datos)
[✗] 3. Visualización de datos (requiere preprocesado completo)
[✗] 4. Exportar datos (requiere visualización de datos)
[✓] 5. Salir 

Seleccione una opción: 1

===================================
         Carga de Datos           
===================================
Seleccione el tipo de archivo a cargar:
  [1] CSV
  [2] Excel
  [3] SQLite
  [4] Volver al menú principal
Seleccione una opción: 1
Ingrese la ruta del archivo: /Users/claudiafernandezvilela/Documents/IA/segundo/primer-cuatri/ingenieria-software/trabajo-segunda-oportunidad/preprocesador-datos-2/titanic_survival.csv
Datos cargados correctamente.
Número de filas: 891
Número de columnas: 12
Primeras 5 filas:
      PassengerId    Survived    Pclass  Name                                                 Sex       Age    SibSp    Parch  Ticket               Fare  Cabin    Embarked
 0              1           0         3  Braund, Mr. Owen Harris                              male       22        1        0  A/5 21171          7.25    nan      S
 1              2           1         1  Cumings, Mrs. John Bradley (Florence Briggs Thayer)  female     38        1        0  PC 17599          71.2833  C85      C
 2              3           1         3  Heikkinen, Miss. Laina                               female     26        0        0  STON/O2. 3101282   7.925   nan      S
 3              4           1         1  Futrelle, Mrs. Jacques Heath (Lily May Peel)         female     35        1        0  113803            53.1     C123     S
 4              5           0         3  Allen, Mr. William Henry                             male       35        0        0  373450             8.05    nan      S

Tipos de datos:
  PassengerId: int64
  Survived: int64
  Pclass: int64
  Name: object
  Sex: object
  Age: float64
  SibSp: int64
  Parch: int64
  Ticket: object
  Fare: float64
  Cabin: object
  Embarked: object
```

### Preprocesado

```
===================================
         Menú Principal           
===================================
[✓] 1. Cargar datos (archivo: titanic_survival.csv)
[-] 2. Preprocesado de datos (selección de columnas requerida)
        [✗] 2.1 Selección de columnas (pendiente)
        [✗] 2.2 Manejo de valores faltantes (requiere selección de columnas)
        [✗] 2.3 Transformación de datos categóricos (requiere manejo de valores faltantes)
        [✗] 2.4 Normalización y escalado (requiere transformación categórica)
        [✗] 2.5 Detección y manejo de valores atípicos (requiere normalización)
[✗] 3. Visualización de datos (requiere preprocesado completo)
[✗] 4. Exportar datos (requiere visualización de datos)
[✓] 5. Salir 

Seleccione una opción: 2
Iniciando preprocesado de datos...
```
#### Selección de columnas
```
Seleccione una opción: 2.1

===================================
         Selección de Columnas    
===================================
Columnas disponibles en los datos:  
  [1] PassengerId
  [2] Survived
  [3] Pclass
  [4] Name
  [5] Sex
  [6] Age
  [7] SibSp
  [8] Parch
  [9] Ticket
  [10] Fare
  [11] Cabin
  [12] Embarked

Ingrese los números de las columnas de entrada (features), separados por comas:1,4,5,6

Ingrese el número de la columna de salida (target): 12

Selección guardada:
Features = ['PassengerId', 'Name', 'Sex', 'Age']
Target = Embarked
```
#### Manejo de valores faltantes
```
===================================
         Manejo de Valores Faltantes
===================================
Se han detectado valores faltantes en las siguientes columnas seleccionadas:
  - Age: 177 valores faltantes
  - Embarked: 2 valores faltantes

Selecciones una estrategia para manejar los valores faltantes:
  [1] Eliminar filas con valores faltantes
  [2] Rellenar con la media de la columna
  [3] Rellenar con la mediana de la columna
  [4] Rellenar con la moda de la columna
  [5] Rellenar con un valor constante
  [6] Volver al menú principal
Seleccione una opción: 2
La columna 'Name' no es numérica. No se pueden rellenar con la media.
La columna 'Sex' no es numérica. No se pueden rellenar con la media.
La columna 'Embarked' no es numérica. No se pueden rellenar con la media.

Valores faltantes rellenados con la media de cada columna numérica.
```


#### Normalización y escalado
```
===================================
         Normalización y Escalado
===================================
Se han detectado columnas numéricas en las variables de entrada seleccionadas: 
  - PassengerId
  - Age

Seleccione una estrategia de normalización: 
  [1] Min-Max Scaling (escala valores entre 0 y 1)
  [2] Z-score Normalization (media 0, desviación estándar 1)
  [3] Volver al menú principal
Seleccione una opción: 1

Normalización completada con Min-Max Scaling.
```

### Menú después de completar el preprocesado
```
===================================
         Menú Principal           
===================================
[✓] 1. Cargar datos (archivo: titanic_survival.csv)
[✓] 2. Preprocesado de datos (completado)
        [✓] 2.1 Selección de columnas (completado)
        [✓] 2.2 Manejo de valores faltantes (completado)
        [✓] 2.3 Transformación de datos categóricos (completado)
        [✓] 2.4 Normalización y escalado (completado)
        [✓] 2.5 Detección y manejo de valores atípicos (completado)
[-] 3. Visualización de datos (pendiente)
[✗] 4. Exportar datos (requiere visualización de datos)
[✓] 5. Salir 
```
### Visualización de datos 
```
Seleccione una opción: 3
=============================
Visualización de Datos
=============================

Seleccione qué tipo de visualización desea generar:
  [1] Resumen estadístico de las variables seleccionadas
  [2] Histogramas de variables numéricas
  [3] Gráficos de dispersión antes y después de la normalización
  [4] Heatmap de correlación de variables numéricas
  [5] Volver al menú principal

Seleccione una opción: 1

Resumen estadístico de las variables seleccionadas:
-------------------------------------------------------------------
Variable      | Media | Mediana | Desviación Est. | Mínimo | Máximo
-------------------------------------------------------------------
PassengerId   | 0.5   | 0.0     | 0.3             | 0.0    | 1.0
Age           | 0.4   | 0.0     | 0.1             | 0.0    | 1.0
```
### Exportar datos
```
===================================
         Exportación de Datos           
===================================
Advertencia: La columna 'Name' no se encuentra en los datos procesados.
Advertencia: La columna 'Sex' no se encuentra en los datos procesados.

Datos a exportar (primeras 5 filas):
      PassengerId       Age  Embarked
 0     0           0.271174  S
 1     0.0011236   0.472229  C
 2     0.00224719  0.321438  S
 3     0.00337079  0.434531  S
 4     0.00449438  0.434531  S
Total de filas: 891, Total de columnas: 903
Seleccione el formato de exportación:
  [1] CSV (.csv)
  [2] Excel (.xlsx)
  [3] Volver al menú principal
Seleccione una opción: 1
Ingrese el nombre del archivo de salida (sin extensión): prueba
Datos exportados correctamente como "prueba.csv".
```
### Salida del programa
```
===================================
         Menú Principal           
===================================
[✓] 1. Cargar datos (archivo: titanic_survival.csv)
[✓] 2. Preprocesado de datos (completado)
        [✓] 2.1 Selección de columnas (completado)
        [✓] 2.2 Manejo de valores faltantes (completado)
        [✓] 2.3 Transformación de datos categóricos (completado)
        [✓] 2.4 Normalización y escalado (completado)
        [✓] 2.5 Detección y manejo de valores atípicos (completado)
[✓] 3. Visualización de datos (completado)
[✓] 4. Exportar datos (completado)
[-] 5. Salir 

Seleccione una opción: 5

===================================
Salir de la Aplicación
===================================
¿Está seguro de que desea salir?
  [1] Sí
  [2] No
Seleccione una opción: 1
Cerrando la aplicación...
Programa finalizado.
```
