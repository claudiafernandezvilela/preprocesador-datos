import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import numpy as np
import io

# Agregar el directorio principal al path para poder importar los módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importación de los módulos a probar
from seleccion_columnas import seleccionar_columnas
from manejo_valores_faltantes import manejo_valores_faltantes
from detectar_valores_atipicos import detectar_valores_atipicos
from normalizado_escalado import normalizar_escalar_datos
from transformar_datos_categoricos import transformar_datos_categoricos

class TestPreprocesado(unittest.TestCase):
    """
    Clase de pruebas unitarias para las funciones de preprocesamiento de datos.
    """

    def setUp(self):
        """
        Configura un DataFrame de prueba que será utilizado en las pruebas.
        """
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

        # Definir columnas de entrada y salida para usar en múltiples pruebas
        self.features = ['Age', 'Sex', 'Ticket', 'Fare']
        self.target = 'SibSp'

    # -------------------------
    # Pruebas para seleccionar_columnas
    # -------------------------

    def test_seleccionar_columnas(self):
        """
        Verifica la selección de columnas válida con índices dados por el usuario.
        """
        with patch('builtins.input', side_effect=['1,4,5', '2']):
            with patch('builtins.print'):
                features, target, success = seleccionar_columnas(self.datos_prueba)
        self.assertEqual(features, ['PassengerId', 'Name', 'Sex'])
        self.assertEqual(target, 'Survived')
        self.assertTrue(success)

    def test_seleccionar_columnas_cancelado(self):
        """
        Verifica el caso en que el usuario cancela la selección de columnas.
        """
        n_cols = len(self.datos_prueba.columns)
        with patch('builtins.input', return_value=str(n_cols + 1)):
            with patch('builtins.print'):
                features, target, success = seleccionar_columnas(self.datos_prueba)
        self.assertIsNone(features)
        self.assertIsNone(target)
        self.assertFalse(success)

    @patch('builtins.input', side_effect=["100", "abc", "1,2", "3"])
    def test_seleccionar_columnas_error_indice(self, mock_input):
        """
        Prueba múltiples entradas inválidas antes de obtener una válida.
        """
        with patch('builtins.print'):
            features, target, success = seleccionar_columnas(self.datos_prueba)
        self.assertEqual(features, ['PassengerId', 'Survived'])
        self.assertEqual(target, 'Pclass')
        self.assertTrue(success)

    # -------------------------
    # Pruebas para manejo_valores_faltantes
    # -------------------------

    def test_manejo_valores_faltantes_sin_nulos(self):
        """
        Verifica el comportamiento cuando no hay valores nulos en las columnas seleccionadas.
        """
        datos_sin_nulos = self.datos_prueba.copy(deep=True)
        datos_sin_nulos['Age'] = datos_sin_nulos['Age'].fillna(25)
        datos_sin_nulos['Cabin'] = datos_sin_nulos['Cabin'].fillna('Unknown')
        with patch('builtins.print') as mock_print:
            datos_procesados, success = manejo_valores_faltantes(datos_sin_nulos, self.features, self.target)
        mock_print.assert_any_call("No se han detectado valores faltantes en las columnas seleccionadas.")
        self.assertTrue(success)

    def test_manejo_valores_faltantes_eliminar_filas(self):
        """
        Verifica la opción de eliminar filas con valores nulos.
        """
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertEqual(len(datos_procesados), 4)
        self.assertTrue(success)

    def test_manejo_valores_faltantes_media(self):
        """
        Verifica el relleno de valores nulos con la media.
        """
        media_age = self.datos_prueba['Age'].mean()
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], media_age)
        self.assertTrue(success)

    def test_manejo_valores_faltantes_mediana(self):
        """
        Verifica el relleno de valores nulos con la mediana.
        """
        mediana_age = self.datos_prueba['Age'].median()
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], mediana_age)
        self.assertTrue(success)

    def test_manejo_valores_faltantes_moda(self):
        """
        Verifica el relleno de valores nulos con la moda.
        """
        with patch('builtins.input', return_value='4'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertTrue(success)

    def test_manejo_valores_faltantes_constante(self):
        """
        Verifica el relleno con un valor constante proporcionado por el usuario.
        """
        with patch('builtins.input', side_effect=['5', '99']):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertFalse(datos_procesados['Age'].isna().any())
        self.assertEqual(datos_procesados.loc[4, 'Age'], 99.0)
        self.assertTrue(success)

    def test_manejo_valores_faltantes_cancelar(self):
        """
        Verifica el comportamiento al cancelar la operación.
        """
        with patch('builtins.input', return_value='6'):
            with patch('builtins.print'):
                datos_procesados, success = manejo_valores_faltantes(self.datos_prueba, self.features, self.target)
        self.assertFalse(success)

    # -------------------------
    # Pruebas para detectar_valores_atipicos
    # -------------------------

    def test_detectar_valores_atipicos_sin_atipicos(self):
        """
        Verifica el comportamiento si no hay valores atípicos.
        """
        datos_sin_atipicos = self.datos_prueba.copy(deep=True)
        with patch('builtins.print') as mock_print:
            datos_procesados, success = detectar_valores_atipicos(datos_sin_atipicos, ['Pclass'], self.target)
        mock_print.assert_any_call("No se han detectado valores atípicos en las columnas seleccionadas.")
        self.assertTrue(success)

    def test_detectar_valores_atipicos_con_atipicos(self):
        """
        Verifica la eliminación de valores atípicos.
        """
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        self.assertEqual(len(datos_procesados), 4)
        self.assertTrue(success)

    def test_detectar_valores_atipicos_reemplazar_mediana(self):
        """
        Verifica el reemplazo de valores atípicos por la mediana.
        """
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0
        mediana_fare = datos_con_atipicos['Fare'].median()
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        self.assertEqual(datos_procesados.loc[0, 'Fare'], mediana_fare)
        self.assertTrue(success)

    def test_detectar_valores_atipicos_mantener(self):
        """
        Verifica que los valores atípicos se mantienen si se selecciona esa opción.
        """
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        self.assertEqual(datos_procesados.loc[0, 'Fare'], 1000.0)
        self.assertTrue(success)

    def test_detectar_valores_atipicos_cancelar(self):
        """
        Verifica el comportamiento si se cancela el manejo de valores atípicos.
        """
        datos_con_atipicos = self.datos_prueba.copy(deep=True)
        datos_con_atipicos.loc[0, 'Fare'] = 1000.0
        with patch('builtins.input', return_value='4'):
            with patch('builtins.print'):
                datos_procesados, success = detectar_valores_atipicos(datos_con_atipicos, ['Fare'], self.target)
        self.assertFalse(success)

    # -------------------------
    # Pruebas para normalizar_escalar_datos
    # -------------------------

    def test_normalizar_escalar_datos_sin_numericas(self):
        """
        Verifica el caso en que no hay columnas numéricas para normalizar.
        """
        with patch('builtins.print') as mock_print:
            datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Sex'], self.target)
        mock_print.assert_any_call("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
        self.assertTrue(success)

    def test_normalizar_escalar_datos_min_max(self):
        """
        Verifica la normalización Min-Max de las columnas numéricas.
        """
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        self.assertTrue(success)
        self.assertTrue((datos_procesados['Fare'] >= 0).all() and (datos_procesados['Fare'] <= 1).all())
        self.assertTrue((datos_procesados['Pclass'] >= 0).all() and (datos_procesados['Pclass'] <= 1).all())

    def test_normalizar_escalar_datos_z_score(self):
        """
        Verifica la normalización Z-score de las columnas numéricas.
        """
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        self.assertTrue(success)
        self.assertAlmostEqual(datos_procesados['Fare'].mean(), 0, places=10)
        self.assertAlmostEqual(datos_procesados['Pclass'].mean(), 0, places=10)

    def test_normalizar_escalar_datos_cancelar(self):
        """
        Verifica el comportamiento al cancelar la operación de normalización.
        """
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = normalizar_escalar_datos(self.datos_prueba, ['Fare', 'Pclass'], self.target)
        self.assertFalse(success)

    # -------------------------
    # Pruebas para transformar_datos_categoricos
    # -------------------------

    def test_transformar_datos_categoricos_sin_categoricas(self):
        """
        Verifica el comportamiento si no hay columnas categóricas para transformar.
        """
        with patch('builtins.print') as mock_print:
            datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Age', 'Fare'], self.target)
        mock_print.assert_any_call("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
        self.assertTrue(success)

    def test_transformar_datos_categoricos_one_hot(self):
        """
        Verifica que se aplique correctamente One-Hot Encoding.
        """
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        self.assertTrue(success)
        self.assertIn('Sex_male', datos_procesados.columns)
        self.assertIn('Sex_female', datos_procesados.columns)

    def test_transformar_datos_categoricos_label_encoding(self):
        """
        Verifica que se aplique correctamente Label Encoding.
        """
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        self.assertTrue(success)
        self.assertTrue(pd.api.types.is_numeric_dtype(datos_procesados['Sex']))

    def test_transformar_datos_categoricos_cancelar(self):
        """
        Verifica el comportamiento al cancelar la transformación categórica.
        """
        with patch('builtins.input', return_value='3'):
            with patch('builtins.print'):
                datos_procesados, success = transformar_datos_categoricos(self.datos_prueba, ['Sex'], self.target)
        self.assertFalse(success)

# Ejecución de pruebas
if __name__ == '__main__':
    unittest.main()
