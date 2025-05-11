import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import sys
import io

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exportar_datos import exportar_datos


class TestExportarDatos(unittest.TestCase):
    """Pruebas unitarias para el módulo exportar_datos."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear un DataFrame de prueba
        self.datos_prueba = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': ['a', 'b', 'c', 'd', 'e'],
            'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        self.features = ['col1', 'col2']
        self.target = 'col3'
    
    @patch('builtins.print')
    def test_exportar_datos_sin_datos(self, mock_print):
        """Prueba la función exportar_datos cuando no hay datos para exportar."""
        resultado = exportar_datos(None, self.features, self.target)
        self.assertFalse(resultado)
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', 'datos_exportados'])
    @patch('pandas.DataFrame.to_csv')
    def test_exportar_datos_csv(self, mock_to_csv, mock_input, mock_print):
        """Prueba la función exportar_datos para exportar a CSV."""
        resultado = exportar_datos(self.datos_prueba, self.features, self.target)
        self.assertTrue(resultado)
        # Verificar que se llamó a to_csv con los parámetros correctos
        mock_to_csv.assert_called_once_with('datos_exportados.csv', index=False)
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['2', 'datos_exportados'])
    @patch('pandas.DataFrame.to_excel')
    def test_exportar_datos_excel(self, mock_to_excel, mock_input, mock_print):
        """Prueba la función exportar_datos para exportar a Excel."""
        resultado = exportar_datos(self.datos_prueba, self.features, self.target)
        self.assertTrue(resultado)
        # Verificar que se llamó a to_excel con los parámetros correctos
        mock_to_excel.assert_called_once_with('datos_exportados.xlsx', index=False)
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['3'])
    def test_exportar_datos_volver(self, mock_input, mock_print):
        """Prueba la función exportar_datos cuando el usuario elige volver al menú principal."""
        resultado = exportar_datos(self.datos_prueba, self.features, self.target)
        self.assertFalse(resultado)
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['5'])  # Opción inválida
    def test_exportar_datos_opcion_invalida(self, mock_input, mock_print):
        """Prueba la función exportar_datos con una opción inválida."""
        resultado = exportar_datos(self.datos_prueba, self.features, self.target)
        self.assertFalse(resultado)
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', ''])  # Nombre de archivo vacío
    def test_exportar_datos_nombre_invalido(self, mock_input, mock_print):
        """Prueba la función exportar_datos con un nombre de archivo inválido."""
        resultado = exportar_datos(self.datos_prueba, self.features, self.target)
        self.assertFalse(resultado)
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()