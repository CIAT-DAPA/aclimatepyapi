import requests
import pandas as pd
import rasterio
import json
import re
import tempfile
import geopandas as gpd
import os

class Geoserver:

    def __init__(self, url_root):
        self.url_root = url_root

    def get_geo_workspaces(self):
        user = os.getenv("GEOSERVER_USER")
        password = os.getenv("GEOSERVER_PASSWORD")
        
        url = f"{self.url_root}/rest/workspaces.json"

        response = requests.get(url, auth=(user, password))
        
        data = json.loads(response.text)
        workspaces_list = data['workspaces']['workspace']
        workspace_df = pd.DataFrame([{'workspace_name': ws['name'], 'workspace_href': ws['href']} for ws in workspaces_list])
        return workspace_df

    # print(get_geo_workspaces("https://geo.aclimate.org/geoserver/"))

    def get_geo_mosaic_name(self, workspace):    
        user = os.getenv("GEOSERVER_USER")
        password = os.getenv("GEOSERVER_PASSWORD")
        
        url = f"{self.url_root}/rest/workspaces/{workspace}/coveragestores.json"

        response = requests.get(url, auth=(user, password))
        
        if response.status_code == 200:
            data = json.loads(response.text)
            if 'coverageStores' in data and 'coverageStore' in data['coverageStores']:
                mosaics_list = data['coverageStores']['coverageStore']
                mosaics_df = pd.DataFrame([{'mosaic_name': ms['name'], 'mosaic_href': ms['href']} for ms in mosaics_list])
                return mosaics_df
        return pd.DataFrame()

    # print(get_geo_mosaic_name("https://geo.aclimate.org/geoserver/", "waterpoints_et"))

    def get_geo_mosaics(self, workspace, mosaic_name, year, month=1, day=1):
        url = f"{self.url_root}{workspace}/ows?service=WCS&request=GetCoverage&version=2.0.1&coverageId={mosaic_name}&format=image/geotiff&subset=Time(\"{year}-{month:02d}-{day:02d}T00:00:00.000Z\")"
        response = requests.get(url)

        if response.status_code == 200:
            # Create a temporary file
            temp_tiff = tempfile.mktemp(suffix=".tif")
            with open(temp_tiff, 'wb') as f:
                f.write(response.content)

            # Load the raster data
            raster_data = rasterio.open(temp_tiff)
            return raster_data.read()

        else:
            match_result = re.findall("<ows:ExceptionText>(.*?)</ows:ExceptionText>", response.text)
            if match_result:
                exception_text = match_result[0]
                print(f"Error making the request. Status code: {response.status_code}\nMsg: {exception_text}")
            else:
                print(f"Error making the request. Status code: {response.status_code}")
            return None

    # print(get_geo_mosaics("https://geo.aclimate.org/geoserver/", "waterpoints_et", "biomass", 2024, 4, 22))

    def get_geo_polygon_name(self, workspace):
        user = os.getenv("GEOSERVER_USER")
        password = os.getenv("GEOSERVER_PASSWORD")

        url = f"{self.url_root}rest/workspaces/{workspace}/datastores.json"
        response = requests.get(url, auth=(user, password))

        if response.status_code == 200:
            data = json.loads(response.text)
            if 'dataStores' in data and 'dataStore' in data['dataStores']:
                polygons_list = data['dataStores']['dataStore']
                polygons_df = pd.DataFrame([{'polygon_name': pg['name'], 'polygon_href': pg['href']} for pg in polygons_list])
                return polygons_df
        return pd.DataFrame()

    # print(get_geo_polygon_name("https://geo.aclimate.org/geoserver/", "fc_cenaos_hn"))

    def get_geo_polygons(self, workspace, polygon_name):
        url = f"{self.url_root}/{workspace}/ows?service=WFS&request=GetFeature&version=2.0.1&typeNames={workspace}:{polygon_name}&outputFormat=application/json"
        response = requests.get(url)

        if response.status_code == 200:
            sf_obj_geoserver = gpd.read_file(response.text)
            return sf_obj_geoserver
        else:
            exception_text = re.search(r'<ows:ExceptionText>(.*?)</ows:ExceptionText>', response.text)
            if exception_text:
                print(f"Error making the request. Status code: {response.status_code}\nMsg: {exception_text.group(1)}")
            else:
                print(f"Error making the request. Status code: {response.status_code}")
            return None
        
    # print(get_geo_polygons("https://geo.aclimate.org/geoserver/", "fc_cenaos_hn", "admin_levels"))