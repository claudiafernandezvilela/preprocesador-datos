import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import io
import sys
import matplotlib.pyplot as plt

# Importamos el módulo a probar
from visualizacion_datos import visualizar_datos

class TestVisualizacionDatos(unittest.TestCase):
    """Clase para probar la funcionalidad de visualización de datos."""
    
    def setUp(self):
        """Prepara los datos de prueba antes de cada test."""
        # Crear un DataFrame de prueba
        self.datos = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10.5, 20.3, 30.1, 40.7, 50.9],
            'categoria': ['A', 'B', 'A', 'C', 'B'],
            'target': [0, 1, 0, 1, 1]
        })
        
        self.features = ['feature1', 'feature2', 'categoria']
        self.target = 'target'
    
    def tearDown(self):
        """Limpia después de cada test."""
        plt.close('all')  # Cerrar todas las figuras de matplotlib
    
    def test_datos_nulos(self):
        """Prueba que la función maneje correctamente cuando los datos son None."""
        resultado = visualizar_datos(None, self.features, self.target)
        self.assertFalse(resultado)
    
    def test_features_nulos(self):
        """Prueba que la función maneje correctamente cuando features es None."""
        resultado = visualizar_datos(self.datos, None, self.target)
        self.assertFalse(resultado)
    
    def test_target_nulo(self):
        """Prueba que la función maneje correctamente cuando target es None."""
        resultado = visualizar_datos(self.datos, self.features, None)
        self.assertFalse(resultado)
    
    def test_columnas_no_existentes(self):
        """Prueba que la función maneje correctamente cuando las columnas no existen."""
        resultado = visualizar_datos(self.datos, ['columna_inexistente'], self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='5')
    def test_opcion_volver_menu(self, mock_input):
        """Prueba la opción de volver al menú principal."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='7')
    def test_opcion_invalida(self, mock_input):
        """Prueba el manejo de una opción inválida."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='abc')
    def test_opcion_no_numerica(self, mock_input):
        """Prueba el manejo de una entrada no numérica."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_resumen_estadistico(self, mock_print, mock_input):
        """Prueba la generación del resumen estadístico."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        
        # Verificar que se llamó a print con información del resumen estadístico
        estadisticas_llamadas = [call for call in mock_print.call_args_list 
                                if "Resumen estadístico" in str(call)]
        self.assertTrue(len(estadisticas_llamadas) > 0)
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='2')
    @patch('matplotlib.pyplot.show')
    def test_histogramas(self, mock_show, mock_input):
        """Prueba la generación de histogramas."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        mock_show.assert_called()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='3')
    @patch('matplotlib.pyplot.show')
    def test_graficos_dispersion(self, mock_show, mock_input):
        """Prueba la generación de gráficos de dispersión."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        # Debería ser llamado una vez por cada variable numérica
        self.assertEqual(mock_show.call_count, 2)  # feature1 y feature2
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='4')
    @patch('matplotlib.pyplot.show')
    def test_heatmap_correlacion(self, mock_show, mock_input):
        """Prueba la generación del heatmap de correlación."""
        resultado = visualizar_datos(self.datos, self.features, self.target)
        
        # Verificar que se llamó a plt.show()
        mock_show.assert_called_once()
        self.assertTrue(resultado)


if __name__ == '__main__':
    unittest.main()