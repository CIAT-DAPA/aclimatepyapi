import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import sys
import os
from io import BytesIO
from rasterio.io import MemoryFile
import geopandas as gpd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aclimate_api.geoserver import Geoserver
from test.mock.mock_geoserver import geo_workspace_mock_data, geo_mosaic_name_mock_data, geo_polygon_name_mock_data, geo_polygon_mock_data

url_root = "https://webapi.aclimate.org/api/"

class TestGeoserver(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geoserver = Geoserver(url_root)

    @patch('requests.get')
    def test_get_geo_workspaces(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geo_workspace_mock_data
        
        result = self.geoserver.get_geo_workspaces()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("workspace_name", result.columns)
        self.assertIn("workspace_href", result.columns)
        self.assertEqual(result.shape[1], 2)
        self.assertEqual(result.shape[0], 8)

    @patch('requests.get')
    def test_get_geo_mosaic_name(self, mock_get):
        workspace = "waterpoints_et"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geo_mosaic_name_mock_data
        
        result = self.geoserver.get_geo_mosaic_name(workspace)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("mosaic_name", result.columns)
        self.assertIn("mosaic_href", result.columns)
        self.assertEqual(result.shape[1], 2)
        self.assertEqual(result.shape[0], 15)
    
    @patch('requests.get')
    def test_get_geo_mosaics(self, mock_get):
        workspace = "waterpoints_et"
        mosaic_name = "biomass"
        year = 2024
        month = 4
        day = 22
        # Create a mock response content (a simple in-memory GeoTIFF)
        mock_tiff = BytesIO()
        with MemoryFile() as memfile:
            with memfile.open(driver='GTiff', height=1, width=1, count=1, dtype=np.uint8) as dst:
                dst.write(np.array([[1]], dtype=np.uint8), 1)
            mock_tiff.write(memfile.read())
        mock_tiff.seek(0)
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_tiff.read()

        result = self.geoserver.get_geo_mosaics(workspace, mosaic_name, year, month, day)

        self.assertIsInstance(result, np.ndarray)

    @patch('requests.get')
    def test_get_geo_polygon_name(self, mock_get):
        workspace = "fc_cenaos_hn"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geo_polygon_name_mock_data
        
        result = self.geoserver.get_geo_polygon_name(workspace)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("polygon_name", result.columns)
        self.assertIn("polygon_href", result.columns)
        self.assertEqual(result.shape[1], 2)
        self.assertEqual(result.shape[0], 8)

    @patch('requests.get')
    def test_get_geo_polygons(self, mock_get):
        workspace = "administrative"
        polygon_name = "ao_adm1"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = geo_polygon_mock_data

        result = self.geoserver.get_geo_polygons(workspace, polygon_name)
        
        self.assertIsInstance(result, gpd.GeoDataFrame)

if __name__ == '__main__':
    unittest.main()