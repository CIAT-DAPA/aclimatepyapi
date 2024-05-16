import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aclimate_api.forecast import Forecast
from test.mock.mock_forecast import forecast_climate_mock_data, forecast_crop_mock_data, forecast_information_mock_data, forecast_subseasonal_mock_data, forecast_climate_previous_mock_data, forecast_crop_previous_mock_data, forecast_crop_ext_mock_data

url_root = "https://webapi.aclimate.org/api/"

class TestForecast(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forecast = Forecast(url_root)

    @patch('requests.get')
    def test_get_forecast_climate(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_climate_mock_data
        
        result = self.forecast.get_forecast_climate(stations)

        self.assertIsInstance(result, dict)
        self.assertIn("probabilities", result)
        self.assertIn("performance", result)
        self.assertIn("scenarios", result)

    @patch('requests.get')
    def test_get_forecast_crop(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_crop_mock_data
        
        result = self.forecast.get_forecast_crop(stations)

        self.assertIsInstance(result, pd.DataFrame)

    @patch('requests.get')
    def test_get_forecast_information(self, mock_get):
        year = 2023
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_information_mock_data
        
        result = self.forecast.get_forecast_information(year)

        self.assertIsInstance(result, pd.DataFrame)

    @patch('requests.get')
    def test_get_forecast_subseasonal(self, mock_get):
        stations = ["63a3744005732d2a14260392"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_subseasonal_mock_data
        
        result = self.forecast.get_forecast_subseasonal(stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 4)
        self.assertEqual(result.shape[1], 8)

    @patch('requests.get')
    def test_get_forecast_climate_previous(self, mock_get):
        forecast = "657006544afb9646da8c6b78"
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_climate_previous_mock_data
        
        result = self.forecast.get_forecast_climate_previous(forecast, stations)

        self.assertIsInstance(result, dict)
        self.assertIn("probabilities", result)
        self.assertIn("performance", result)
        self.assertIn("scenarios", result)
        self.assertEqual(result["probabilities"].shape[1], 7)
        self.assertEqual(result["performance"].shape[1], 5)
        self.assertEqual(result["scenarios"].shape[1], 6)

    @patch('requests.get')
    def test_get_forecast_crop_previous(self, mock_get):
        forecast = "657006544afb9646da8c6b78"
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_crop_previous_mock_data
        
        result = self.forecast.get_forecast_crop_previous(forecast, stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(result.shape[0], 0)
        self.assertEqual(result.shape[1], 19)

    @patch('requests.get')
    def test_get_forecast_crop_exc(self, mock_get):
        stations = ["58504f1a006cb93ed40eebe2"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = forecast_crop_ext_mock_data
        
        result = self.forecast.get_forecast_crop_exc(stations)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(result.shape[0], 0)
        self.assertEqual(result.shape[1], 19)

if __name__ == '__main__':
    unittest.main()