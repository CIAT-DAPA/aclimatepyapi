import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aclimate_api.geographic import Geographic
from test.mock.mock_geographic import geographic_country_mock_data, geographic_mock_data, geographic_ws_mock_data

url_root = "https://webapi.aclimate.org/api/"

class TestGeographic(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geographic = Geographic(url_root)

    @patch('requests.get')
    def test_get_geographic_country(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geographic_country_mock_data
        
        result = self.geographic.get_geographic_country()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 9)
        self.assertEqual(result.shape[1], 3)

    @patch('requests.get')
    def test_get_geographic(self, mock_get):
        country_id = "61e59d829d5d2486e18d2ea8"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geographic_mock_data
        
        result = self.geographic.get_geographic(country_id)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 3)
        self.assertEqual(result.shape[1], 13)

    @patch('requests.get')
    def test_get_geographic_ws(self, mock_get):
        country_id = "6438525c843fb30d41311d25"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geographic_ws_mock_data
        
        result = self.geographic.get_geographic_ws(country_id)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 14)
        self.assertEqual(result.shape[1], 7)

if __name__ == '__main__':
    unittest.main()
