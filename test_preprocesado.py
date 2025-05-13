import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import numpy as np
import io

# Agregar el directorio principal al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos los módulos que vamos a probar
from seleccion_columnas import seleccionar_columnas
from manejo_valores_faltantes import manejo_valores_faltantes
from detectar_valores_atipicos import detectar_valores_atipicos
from normalizado_escalado import normalizar_escalar_datos
from transformar_datos_categoricos import transformar_datos_categoricos

class TestPreprocesado(unittest.TestCase):
    # Creamos un DataFrame de prueba con la estructura proporcionada
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
        
        # Definimos las columnas de características y objetivo que usaremos en las pruebas
        self.features = ['Age', 'Sex', 'Ticket', 'Fare']
        self.target = 'SibSp'

    # Pruebas para seleccionar_columnas
    def test_seleccionar_columnas(self):
        with patch('builtins.input', side_effect=['1,4,5', '2']):
            with patch('builtins.print'):
                features, target, success = seleccionar_columnas(self.datos_prueba)
        
        self.assertEqual(features, ['PassengerId', 'Name', 'Sex'])
        self.assertEqual(target, 'Survived')
        self.assertTrue(success)
    
    def test_seleccionar_columnas_cancelado(self):
        # Simulamos cancelar la operación (último índice + 1)
        n_cols = len(self.datos_prueba.columns)
        with patch('builtins.input', return_value=str(n_cols + 1)):
            with patch('builtins.print'):
                features, target, success = seleccionar_columnas(self.datos_prueba)
        
        self.assertIsNone(features)
        self.assertIsNone(target)
        self.assertFalse(success)
    
    @patch('builtins.input', side_effect=["100", "abc", "1,2", "3"])  # Se necesitan al menos dos inputs válidos
    def test_seleccionar_columnas_error_indice(self, mock_input):
        with patch('builtins.print'):
            features, target, success = seleccionar_columnas(self.datos_prueba)
        self.assertEqual(features, ['PassengerId', 'Survived'])
        self.assertEqual(target, 'Pclass')
        self.assertTrue(success)
    
    # Pruebas para manejo_valores_faltantes
    def test_manejo_valores_faltantes_sin_nulos(self):
        # Crear un dataset sin valores nulos
        datos_sin_nulos = self.datos_prueba.copy(deep=True)
        datos_sin_nulos['Age'] = datos_sin_nulos['Age'].fillna(25)
        datos_sin_nulos['Cabin'] = datos_sin_nulos['Cabin'].fillna('Unknown')

        with patch('builtins.print') as mock_print:
            datos_procesados, success = manejo_valores_faltantes(datos_sin_nulos, self.features, self.target)
        
        mock_print.assert_any_call("No se han detectado valores faltantes en las columnas seleccionadas.")
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_eliminar_filas(self):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que se eliminaron las filas con valores nulos
        self.assertEqual(len(datos_procesados), 4)  # Una fila menos (la que tenía Age=np.nan)
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_media(self):
        media_age = self.datos_prueba['Age'].mean()
        
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que se rellenaron los valores nulos con la media
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], media_age)
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_mediana(self):
        mediana_age = self.datos_prueba['Age'].median()
        
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que se rellenaron los valores nulos con la mediana
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], mediana_age)
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_moda(self):
        with patch('builtins.input', return_value='4'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que se rellenaron los valores nulos
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_constante(self):
        with patch('builtins.input', side_effect=['5', '99']):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que se rellenaron los valores nulos con la constante
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], 99.0)
        self.assertTrue(success)
    
    def test_manejo_valores_faltantes_cancelar(self):
        with patch('builtins.input', return_value='6'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        
        # Verificamos que la operación fue cancelada
        self.assertFalse(success)
    
    # Pruebas para detectar_valores_atipicos
    def test_detectar_valores_atipicos_sin_atipicos(self):
        # Crear dataset sin valores atípicos
        datos_sin_atipicos = self.datos_prueba.copy(deep=True)
        
        with patch('builtins.print') as mock_print:
            datos_procesados, success = detectar_valores_atipicos(datos_sin_atipicos, ['Pclass'], self.target)
        
        # Para la columna Pclass no deberían detectarse valores atípicos
        mock_print.assert_any_call("No se han detectado valores atípicos en las columnas numéricas seleccionadas.")
        self.assertTrue(success)
    
    def test_detectar_valores_atipicos_con_atipicos(self):
        # Crear dataset con valores atípicos
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0  # Valor atípico
        
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        
        # Verificamos que se eliminó la fila con el valor atípico
        self.assertEqual(len(datos_procesados), 4)  # Una fila menos
        self.assertTrue(success)
    
    def test_detectar_valores_atipicos_reemplazar_mediana(self):
        # Crear dataset con valores atípicos
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0  # Valor atípico
        mediana_fare = datos_con_atipicos['Fare'].median()
        
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        
        # Verificamos que se reemplazó el valor atípico con la mediana
        self.assertEqual(datos_procesados.loc[0, 'Fare'], mediana_fare)
        self.assertTrue(success)
    
    def test_detectar_valores_atipicos_mantener(self):
        # Crear dataset con valores atípicos
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0  # Valor atípico
        
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        
        # Verificamos que se mantuvo el valor atípico
        self.assertEqual(datos_procesados.loc[0, 'Fare'], 1000.0)
        self.assertTrue(success)
    
    def test_detectar_valores_atipicos_cancelar(self):
        # Crear dataset con valores atípicos
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0  # Valor atípico
        
        with patch('builtins.input', return_value='4'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        
        # Verificamos que la operación fue cancelada
        self.assertFalse(success)
    
    # Pruebas para normalizar_escalar_datos
    def test_normalizar_escalar_datos_sin_numericas(self):
        with patch('builtins.print') as mock_print:
            datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Sex'], self.target)
        
        # No hay columnas numéricas, así que no se debe aplicar normalización
        mock_print.assert_any_call("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
        self.assertTrue(success)
    
    def test_normalizar_escalar_datos_min_max(self):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        
        # Verificar que la normalización Min-Max se aplicó correctamente
        self.assertTrue(success)
        
        self.assertTrue((datos_procesados['Fare'] >= 0).all() and (datos_procesados['Fare'] <= 1).all())
        self.assertTrue((datos_procesados['Pclass'] >= 0).all() and (datos_procesados['Pclass'] <= 1).all())
    
    def test_normalizar_escalar_datos_z_score(self):
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        
        # Verificar que la normalización Z-score se aplicó correctamente
        self.assertTrue(success)
        
        self.assertAlmostEqual(datos_procesados['Fare'].mean(), 0, places=10)
        self.assertAlmostEqual(datos_procesados['Pclass'].mean(), 0, places=10)
    
    def test_normalizar_escalar_datos_cancelar(self):
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        
        # Verificar que la operación fue cancelada
        self.assertFalse(success)
    
    # Pruebas para transformar_datos_categoricos
    def test_transformar_datos_categoricos_sin_categoricas(self):
        with patch('builtins.print') as mock_print:
            datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Age', 'Fare'], self.target)
        
        # No hay columnas categóricas, así que no se debe aplicar transformación
        mock_print.assert_any_call("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
        self.assertTrue(success)
    
    def test_transformar_datos_categoricos_one_hot(self):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        
        # Verificar que se aplicó correctamente el One-Hot Encoding
        self.assertTrue(success)
        self.assertIn('Sex_male', datos_procesados.columns)
        self.assertIn('Sex_female', datos_procesados.columns)
    
    def test_transformar_datos_categoricos_label_encoding(self):
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        
        # Verificar que se aplicó correctamente el Label Encoding
        self.assertTrue(success)
        # Los valores únicos deberían ser numéricos (0 para 'female' y 1 para 'male', o viceversa)
        self.assertTrue(pd.api.types.is_numeric_dtype(datos_procesados['Sex']))
    
    def test_transformar_datos_categoricos_cancelar(self):
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        
        # Verificar que la operación fue cancelada
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()