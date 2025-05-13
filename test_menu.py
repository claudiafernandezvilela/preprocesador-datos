import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import sys
import io

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menu import simbolo, mostrar_menu, mostrar_dialogo_salir


class TestMenu(unittest.TestCase):
    """Pruebas unitarias para el módulo menu."""
    
    def test_simbolo(self):
        """Prueba la función simbolo que determina el estado de cada opción del menú."""
        # Paso actual menor que el requerido (opción bloqueada)
        self.assertEqual(simbolo(3, 1), '✗')
        
        # Paso actual igual al requerido (opción actual)
        self.assertEqual(simbolo(2, 2), '-')
        
        # Caso especial para el paso 2 (preprocesado)
        self.assertEqual(simbolo(2, 2.5), '-')
        
        # Paso actual mayor que el requerido (opción completada)
        self.assertEqual(simbolo(1, 3), '✓')
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_mostrar_menu_sin_datos(self, mock_input, mock_print):
        """Prueba la función mostrar_menu cuando no hay datos cargados."""
        opcion = mostrar_menu(1)
        self.assertEqual(opcion, '1')
        # Verificar que se llamó a print al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_mostrar_menu_con_datos_csv(self, mock_input, mock_print):
        """Prueba la función mostrar_menu cuando hay datos CSV cargados."""
        opcion = mostrar_menu(2, ruta='datos/ejemplo.csv', tipo_archivo='CSV')
        self.assertEqual(opcion, '2')
        # Verificar que se llamó a print al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_mostrar_dialogo_salir_si(self, mock_input, mock_print):
        """Prueba la función mostrar_dialogo_salir cuando el usuario elige 'Sí'."""
        resultado = mostrar_dialogo_salir()
        self.assertTrue(resultado)
        # Verificar que se llamó a print al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_mostrar_dialogo_salir_no(self, mock_input, mock_print):
        """Prueba la función mostrar_dialogo_salir cuando el usuario elige 'No'."""
        resultado = mostrar_dialogo_salir()
        self.assertFalse(resultado)
        # Verificar que se llamó a print al menos una vez
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()