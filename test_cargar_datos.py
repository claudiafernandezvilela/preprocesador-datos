import unittest
import os
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock
import sys
import io
from contextlib import contextmanager

# Determinar la ruta absoluta del directorio raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Añadir el directorio raíz del proyecto al path de Python
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importar las funciones que estamos probando
from cargar_datos import cargar_datos, cargar_csv, cargar_excel, cargar_sqlite, mostrar_info_dataset

@contextmanager
def capturar_salida():
    """
    Contexto para capturar la salida estándar.
    """
    nuevo_stdout = io.StringIO()
    viejo_stdout = sys.stdout
    try:
        sys.stdout = nuevo_stdout
        yield nuevo_stdout
    finally:
        sys.stdout = viejo_stdout

class TestCargarDatos(unittest.TestCase):
    """
    Clase para probar las funciones del módulo cargar_datos.py
    """
    
    def setUp(self):
        """
        Configuración previa para las pruebas.
        """
        # Crear un DataFrame de prueba
        self.df_prueba = pd.DataFrame({
            'columna1': [1, 2, 3, 4, 5],
            'columna2': ['a', 'b', 'c', 'd', 'e']
        })
        
        # Crear archivos temporales para pruebas con las extensiones correctas
        self.ruta_csv = "test_data.csv"
        self.ruta_excel = "test_data.xlsx"
        self.ruta_sqlite = "test_data.db"
        
        # Guardar el DataFrame de prueba en diferentes formatos
        self.df_prueba.to_csv(self.ruta_csv, index=False)
        self.df_prueba.to_excel(self.ruta_excel, index=False)
        
        # Crear una base de datos SQLite con el DataFrame
        conn = sqlite3.connect(self.ruta_sqlite)
        self.df_prueba.to_sql("tabla_prueba", conn, if_exists="replace", index=False)
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
        pd.testing.assert_frame_equal(datos, self.df_prueba)
    
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
        pd.testing.assert_frame_equal(datos, self.df_prueba)
    
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
        pd.testing.assert_frame_equal(datos.reset_index(drop=True), self.df_prueba.reset_index(drop=True))
    
    def test_mostrar_info_dataset(self):
        """
        Probar que la función mostrar_info_dataset muestra la información correcta.
        """
        with capturar_salida() as salida:
            mostrar_info_dataset(self.df_prueba, "ruta_test", "CSV")
            contenido = salida.getvalue()
            
            # Verificar que la salida contiene información básica
            self.assertIn("Datos cargados correctamente", contenido)
            self.assertIn(f"Número de filas: {self.df_prueba.shape[0]}", contenido)
            self.assertIn(f"Número de columnas: {self.df_prueba.shape[1]}", contenido)
            self.assertIn("Primeras 5 filas", contenido)
            self.assertIn("Tipos de datos", contenido)

if __name__ == '__main__':
    unittest.main()