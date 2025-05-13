import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import sys
import io

# Añadir el directorio raíz del proyecto al path de Python
# Esto asegura que los módulos del proyecto puedan ser importados correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar las funciones del módulo `menu` que serán probadas
from menu import simbolo, mostrar_menu, mostrar_dialogo_salir


class TestMenu(unittest.TestCase):
    """Pruebas unitarias para el módulo menu."""

    def test_simbolo(self):
        """
        Prueba la función `simbolo` que determina el estado de cada opción del menú.
        """
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
        """
        Prueba la función `mostrar_menu` cuando no hay datos cargados.
        """
        # Simular que el usuario selecciona la opción '1'
        opcion = mostrar_menu(1)
        self.assertEqual(opcion, '1')  # Verificar que la opción seleccionada es la esperada
        # Verificar que se llamó a `print` al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_mostrar_menu_con_datos_csv(self, mock_input, mock_print):
        """
        Prueba la función `mostrar_menu` cuando hay datos CSV cargados.
        """
        # Simular que el usuario selecciona la opción '2' y que hay un archivo CSV cargado
        opcion = mostrar_menu(2, ruta='datos/ejemplo.csv', tipo_archivo='CSV')
        self.assertEqual(opcion, '2')  # Verificar que la opción seleccionada es la esperada
        # Verificar que se llamó a `print` al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_mostrar_dialogo_salir_si(self, mock_input, mock_print):
        """
        Prueba la función `mostrar_dialogo_salir` cuando el usuario elige 'Sí'.
        """
        # Simular que el usuario selecciona '1' (Sí)
        resultado = mostrar_dialogo_salir()
        self.assertTrue(resultado)  # Verificar que el resultado es True
        # Verificar que se llamó a `print` al menos una vez
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('builtins.input', return_value='2')
    def test_mostrar_dialogo_salir_no(self, mock_input, mock_print):
        """
        Prueba la función `mostrar_dialogo_salir` cuando el usuario elige 'No'.
        """
        # Simular que el usuario selecciona '2' (No)
        resultado = mostrar_dialogo_salir()
        self.assertFalse(resultado)  # Verificar que el resultado es False
        # Verificar que se llamó a `print` al menos una vez
        mock_print.assert_called()


if __name__ == '__main__':
    # Ejecutar las pruebas si el archivo se ejecuta directamente
    unittest.main()