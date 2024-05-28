import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aclimate_api.agronomy import Agronomy
from test.mock.mock_agronomy import agronomy_mock_data

url_root = "https://webapi.aclimate.org/api/"

class TestAgronomy(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agronomy = Agronomy(url_root)

    @patch('requests.get')
    def test_get_agronomy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = agronomy_mock_data
        
        result = self.agronomy.get_agronomy()

        self.assertIsInstance(result, dict)
        self.assertIn('cultivars', result)
        self.assertIn('soils', result)
        self.assertIsInstance(result['cultivars'], pd.DataFrame)
        self.assertIsInstance(result['soils'], pd.DataFrame)
        self.assertEqual(len(result['cultivars']), 2)
        self.assertEqual(len(result['soils']), 2)

if __name__ == '__main__':
    unittest.main()
