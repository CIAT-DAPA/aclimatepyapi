import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aclimate_api.historical import Historical
from test.mock.mock_historical import historical_climatology_mock_data, historical_climatic_mock_data, yield_years_mock_data, yield_mock_data

url_root = "https://webapi.aclimate.org/api/"

class TestHistorical(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.historical = Historical(url_root)

    @patch('requests.get')
    def test_get_historical_climatology(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = historical_climatology_mock_data
        
        result = self.historical.get_historical_climatology(stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(result.shape[0], 48)
        self.assertEqual(result.shape[1], 4)

    @patch('requests.get')
    def test_get_historical_historicalclimatic(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = historical_climatic_mock_data
        
        result = self.historical.get_historical_historicalclimatic(stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(result.shape[0], 35)
        self.assertEqual(result.shape[1], 5)

    @patch('requests.get')
    def test_get_historical_historicalyieldyears(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = yield_years_mock_data
        
        result = self.historical.get_historical_historicalyieldyears(stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(result.shape[0], 0)
        self.assertEqual(result.shape[1], 1)

    @patch('requests.get')
    def test_get_historical_historicalyield(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        years = ["2023"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = yield_mock_data
        
        result = self.historical.get_historical_historicalyield(stations, years)

        self.assertIsInstance(result, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
