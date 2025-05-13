import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import io
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from contextlib import contextmanager

# Asegurar que el directorio raíz esté en el path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importar funciones desde los módulos
from cargar_datos import cargar_datos, cargar_csv, cargar_excel, cargar_sqlite, mostrar_info_dataset
from visualizacion_datos import visualizar_datos
from exportar_datos import exportar_datos

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.datos_prueba = pd.DataFrame({
            'PassengerId': [1, 2, 3, 4, 5],
            'Survived': [0, 1, 1, 1, 0],
            'Pclass': [3, 1, 3, 1, 3],
            'Name': ['Braund, Mr. Owen Harris', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 
                    'Heikkinen, Miss. Laina', 'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 'Allen, Mr. William Henry'],
            'Sex': ['male', 'female', 'female', 'female', 'male'],
            'Age': [22, 38, 26, 35, np.nan],
            'SibSp': [1, 1, 0, 1, 0],
            'Parch': [0, 0, 0, 0, 0],
            'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450'],
            'Fare': [7.25, 71.28, 7.92, 53.10, 8.05],
            'Cabin': [np.nan, 'C85', np.nan, 'C123', np.nan],
            'Embarked': ['S', 'C', 'S', 'S', 'S']
        })
        self.features = ['Age', 'Sex', 'Ticket', 'Fare']
        self.target = 'SibSp'

@contextmanager
def capturar_salida():
    nuevo_stdout = io.StringIO()
    viejo_stdout = sys.stdout
    try:
        sys.stdout = nuevo_stdout
        yield nuevo_stdout
    finally:
        sys.stdout = viejo_stdout

class TestCargarDatos(BaseTestCase):
    """
    Clase para probar las funciones del módulo cargar_datos.py
    """
    
    def setUp(self):
        """
        Configuración previa para las pruebas.
        """
        super().setUp()
        
        # Crear archivos temporales para pruebas con las extensiones correctas
        self.ruta_csv = "test_data.csv"
        self.ruta_excel = "test_data.xlsx"
        self.ruta_sqlite = "test_data.db"
        
        # Guardar el DataFrame de prueba en diferentes formatos
        self.datos_prueba.to_csv(self.ruta_csv, index=False)
        self.datos_prueba.to_excel(self.ruta_excel, index=False)
        
        # Crear una base de datos SQLite con el DataFrame
        conn = sqlite3.connect(self.ruta_sqlite)
        self.datos_prueba.to_sql("tabla_prueba", conn, if_exists="replace", index=False)
        conn.close()
    
    def tearDown(self):
        """
        Limpieza después de las pruebas.
        """
        # Eliminar archivos temporales
        if os.path.exists(self.ruta_csv):
            os.remove(self.ruta_csv)
        if os.path.exists(self.ruta_excel):
            os.remove(self.ruta_excel)
        if os.path.exists(self.ruta_sqlite):
            os.remove(self.ruta_sqlite)
    
    @patch('builtins.input', side_effect=['4'])
    def test_cargar_datos_opcion_volver(self, mock_input):
        """
        Probar que la función cargar_datos devuelve (None, None, None) cuando se selecciona volver al menú.
        """
        datos, ruta, tipo = cargar_datos()
        self.assertIsNone(datos)
        self.assertIsNone(ruta)
        self.assertIsNone(tipo)
    
    @patch('builtins.input', side_effect=['5'])  # Opción inválida
    def test_cargar_datos_opcion_invalida(self, mock_input):
        """
        Probar que la función cargar_datos maneja correctamente una opción inválida.
        """
        datos, ruta, tipo = cargar_datos()
        self.assertIsNone(datos)
        self.assertIsNone(ruta)
        self.assertIsNone(tipo)
    
    @patch('builtins.input', side_effect=['archivo_inexistente.csv'])
    def test_cargar_csv_archivo_inexistente(self, mock_input):
        """
        Probar que la función cargar_csv maneja correctamente un archivo inexistente.
        """
        datos, ruta, tipo = cargar_csv()
        self.assertIsNone(datos)
        self.assertIsNone(ruta)
        self.assertIsNone(tipo)
    
    @patch('builtins.input', side_effect=[os.path.abspath('test_data.csv')])
    def test_cargar_csv_archivo_valido(self, mock_input):
        """
        Probar que la función cargar_csv carga correctamente un archivo CSV válido.
        """
        datos, ruta, tipo = cargar_csv()
        self.assertIsNotNone(datos)
        self.assertEqual(ruta, os.path.abspath('test_data.csv'))
        self.assertEqual(tipo, 'CSV')
        # Verificar que los datos sean iguales al DataFrame original
        pd.testing.assert_frame_equal(datos, self.datos_prueba)
    
    @patch('builtins.input', side_effect=['archivo_inexistente.xlsx'])
    def test_cargar_excel_archivo_inexistente(self, mock_input):
        """
        Probar que la función cargar_excel maneja correctamente un archivo inexistente.
        """
        datos, ruta, tipo = cargar_excel()
        self.assertIsNone(datos)
        self.assertIsNone(ruta)
        self.assertIsNone(tipo)
    
    @patch('builtins.input', side_effect=[os.path.abspath('test_data.xlsx'), '1'])
    def test_cargar_excel_archivo_valido(self, mock_input):
        """
        Probar que la función cargar_excel carga correctamente un archivo Excel válido.
        """
        datos, ruta, tipo = cargar_excel()
        self.assertIsNotNone(datos)
        self.assertEqual(ruta, os.path.abspath('test_data.xlsx'))
        self.assertEqual(tipo, 'Excel')
        # Verificar que los datos sean iguales al DataFrame original
        pd.testing.assert_frame_equal(datos, self.datos_prueba)
    
    @patch('builtins.input', side_effect=['archivo_inexistente.db'])
    def test_cargar_sqlite_archivo_inexistente(self, mock_input):
        """
        Probar que la función cargar_sqlite maneja correctamente un archivo inexistente.
        """
        datos, ruta, tipo = cargar_sqlite()
        self.assertIsNone(datos)
        self.assertIsNone(ruta)
        self.assertIsNone(tipo)
    
    @patch('builtins.input', side_effect=[os.path.abspath('test_data.db'), '1'])
    def test_cargar_sqlite_archivo_valido(self, mock_input):
        """
        Probar que la función cargar_sqlite carga correctamente una base de datos SQLite válida.
        """
        datos, ruta, tipo = cargar_sqlite()
        self.assertIsNotNone(datos)
        self.assertTrue('test_data.db|tabla_prueba' in ruta)
        self.assertEqual(tipo, 'SQLite')
        # Verificar que los datos sean iguales al DataFrame original
        pd.testing.assert_frame_equal(datos.reset_index(drop=True), self.datos_prueba.reset_index(drop=True))
    
    def test_mostrar_info_dataset(self):
        """
        Probar que la función mostrar_info_dataset muestra la información correcta.
        """
        with capturar_salida() as salida:
            mostrar_info_dataset(self.datos_prueba, "ruta_test", "CSV")
            contenido = salida.getvalue()
            
            # Verificar que la salida contiene información básica
            self.assertIn("Datos cargados correctamente", contenido)
            self.assertIn(f"Número de filas: {self.datos_prueba.shape[0]}", contenido)
            self.assertIn(f"Número de columnas: {self.datos_prueba.shape[1]}", contenido)
            self.assertIn("Primeras 5 filas", contenido)
            self.assertIn("Tipos de datos", contenido)

class TestExportarDatos(BaseTestCase):
    """Clase para probar la funcionalidad de exportación de datos."""
    def setUp(self):
        """Prepara los datos de prueba antes de cada test."""
        super().setUp()
    
    @patch('builtins.print')
    def test_exportar_datos_sin_datos(self, mock_print):
        self.assertFalse(exportar_datos(None, self.features, self.target))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', 'datos_exportados'])
    @patch('pandas.DataFrame.to_csv')
    def test_exportar_datos_csv(self, mock_to_csv, mock_input, mock_print):
        self.assertTrue(exportar_datos(self.datos_prueba, self.features, self.target))
        mock_to_csv.assert_called_once_with('datos_exportados.csv', index=False)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['2', 'datos_exportados'])
    @patch('pandas.DataFrame.to_excel')
    def test_exportar_datos_excel(self, mock_to_excel, mock_input, mock_print):
        self.assertTrue(exportar_datos(self.datos_prueba, self.features, self.target))
        mock_to_excel.assert_called_once_with('datos_exportados.xlsx', index=False)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['3'])
    def test_exportar_datos_volver(self, mock_input, mock_print):
        self.assertFalse(exportar_datos(self.datos_prueba, self.features, self.target))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['5'])
    def test_exportar_datos_opcion_invalida(self, mock_input, mock_print):
        self.assertFalse(exportar_datos(self.datos_prueba, self.features, self.target))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', ''])
    def test_exportar_datos_nombre_invalido(self, mock_input, mock_print):
        self.assertFalse(exportar_datos(self.datos_prueba, self.features, self.target))

class TestVisualizacionDatos(BaseTestCase):
    """Clase para probar la funcionalidad de visualización de datos."""
    
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        """Limpia después de cada test."""
        plt.close('all')  # Cerrar todas las figuras de matplotlib
    
    def test_datos_nulos(self):
        """Prueba que la función maneje correctamente cuando los datos son None."""
        resultado = visualizar_datos(None, self.features, self.target)
        self.assertFalse(resultado)
    
    def test_features_nulos(self):
        """Prueba que la función maneje correctamente cuando features es None."""
        resultado = visualizar_datos(self.datos_prueba, None, self.target)
        self.assertFalse(resultado)
    
    def test_target_nulo(self):
        """Prueba que la función maneje correctamente cuando target es None."""
        resultado = visualizar_datos(self.datos_prueba, self.features, None)
        self.assertFalse(resultado)
    
    def test_columnas_no_existentes(self):
        """Prueba que la función maneje correctamente cuando las columnas no existen."""
        resultado = visualizar_datos(self.datos_prueba, ['columna_inexistente'], self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='5')
    def test_opcion_volver_menu(self, mock_input):
        """Prueba la opción de volver al menú principal."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='7')
    def test_opcion_invalida(self, mock_input):
        """Prueba el manejo de una opción inválida."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='abc')
    def test_opcion_no_numerica(self, mock_input):
        """Prueba el manejo de una entrada no numérica."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_resumen_estadistico(self, mock_print, mock_input):
        """Prueba la generación del resumen estadístico."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        
        # Verificar que se llamó a print con información del resumen estadístico
        estadisticas_llamadas = [call for call in mock_print.call_args_list 
                                if "Resumen estadístico" in str(call)]
        self.assertTrue(len(estadisticas_llamadas) > 0)
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='2')
    @patch('matplotlib.pyplot.show')
    def test_histogramas(self, mock_show, mock_input):
        """Prueba la generación de histogramas."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        mock_show.assert_called()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='3')
    @patch('matplotlib.pyplot.show')
    def test_graficos_dispersion(self, mock_show, mock_input):
        """Prueba la generación de gráficos de dispersión."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        # Debería ser llamado una vez por cada variable numérica
        self.assertEqual(mock_show.call_count, 2)  # feature1 y feature2
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='4')
    @patch('matplotlib.pyplot.show')
    def test_heatmap_correlacion(self, mock_show, mock_input):
        """Prueba la generación del heatmap de correlación."""
        resultado = visualizar_datos(self.datos_prueba, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        mock_show.assert_called_once()
        self.assertTrue(resultado)

if __name__ == '__main__':
    unittest.main()
