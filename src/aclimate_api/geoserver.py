import requests
import pandas as pd
import rasterio
import json
import re
import tempfile
import geopandas as gpd

class Geoserver:

    def __init__(self, url_root):
        self.url_root = url_root

    def get_geo_workspaces(self, user, password):
        """
        Retrieves the list of GeoServer workspaces.

        Args:
            user (str): The username for the GeoServer instance.
            password (str): The password for the GeoServer instance.

        Returns:
            pandas.DataFrame: A DataFrame containing the workspace names and their corresponding hrefs.
        """

        if not user or not password:
            print("Error: Missing GeoServer credentials")
            return None

        try:
            url = f"{self.url_root}/rest/workspaces.json"
            response = requests.get(url, auth=(user, password))
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return pd.DataFrame()
        
        if response.status_code == 401:
            print("Error: Unauthorized. Check your GeoServer credentials.")
            return None

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print("Error: Failed to decode the response as JSON")
            print(e)
            return None

        try:
            workspaces_list = data['workspaces']['workspace']
            workspace_df = pd.DataFrame([{'workspace_name': ws['name'], 'workspace_href': ws['href']} for ws in workspaces_list])
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        return workspace_df

    # print(get_geo_workspaces("https://geo.aclimate.org/geoserver/"))

    def get_geo_mosaic_name(self, workspace, user, password):
        """
        Retrieves the names and hrefs of the mosaics in the specified GeoServer workspace.

        Args:
            workspace (str): The name of the GeoServer workspace.
            user (str): The username for the GeoServer instance.
            password (str): The password for the GeoServer instance.

        Returns:
            pandas.DataFrame: A DataFrame containing the mosaic names and hrefs, or an empty DataFrame if there was an error.
        """

        if not user or not password:
            print("Error: Missing GeoServer credentials")
            return pd.DataFrame()

        try:
            url = f"{self.url_root}/rest/workspaces/{workspace}/coveragestores.json"
            response = requests.get(url, auth=(user, password))
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return pd.DataFrame()

        if response.status_code == 401:
            print("Error: Unauthorized. Check your GeoServer credentials.")
            return pd.DataFrame()

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print("Error: Failed to decode the response as JSON")
            print(e)
            return pd.DataFrame()

        if 'coverageStores' in data and 'coverageStore' in data['coverageStores']:
            try:
                mosaics_list = data['coverageStores']['coverageStore']
                mosaics_df = pd.DataFrame([{'mosaic_name': ms['name'], 'mosaic_href': ms['href']} for ms in mosaics_list])
            except KeyError as e:
                print("Error: Missing key in data")
                print(e)
                return pd.DataFrame()
            return mosaics_df

        return pd.DataFrame()

    # print(get_geo_mosaic_name("https://geo.aclimate.org/geoserver/", "waterpoints_et"))

    def get_geo_mosaics(self, workspace, mosaic_name, year, month=1, day=1):
        """
        Retrieves a geospatial mosaic from a GeoServer instance.

        Args:
            workspace (str): The name of the workspace where the mosaic is located.
            mosaic_name (str): The name of the mosaic to retrieve.
            year (int): The year of the mosaic to retrieve.
            month (int, optional): The month of the mosaic to retrieve. Defaults to 1.
            day (int, optional): The day of the mosaic to retrieve. Defaults to 1.

        Returns:
            numpy.ndarray or None: The raster data of the retrieved mosaic as a NumPy array, or None if an error occurred.
        """
        try:
            url = f"{self.url_root}{workspace}/ows?service=WCS&request=GetCoverage&version=2.0.1&coverageId={mosaic_name}&format=image/geotiff&subset=Time(\"{year}-{month:02d}-{day:02d}T00:00:00.000Z\")"
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return None

        if response.status_code == 200:
            try:
                # Create a temporary file
                temp_tiff = tempfile.mktemp(suffix=".tif")
                with open(temp_tiff, 'wb') as f:
                    f.write(response.content)

                # Load the raster data
                raster_data = rasterio.open(temp_tiff)
                return raster_data.read()
            except Exception as e:
                print("Error: Failed to write the response content to a temporary file or load the raster data")
                print(e)
                return None

        else:
            match_result = re.findall("<ows:ExceptionText>(.*?)</ows:ExceptionText>", response.text)
            if match_result:
                exception_text = match_result[0]
                print(f"Error making the request. Status code: {response.status_code}\nMsg: {exception_text}")
            else:
                print(f"Error making the request. Status code: {response.status_code}")
            return None

    # print(get_geo_mosaics("https://geo.aclimate.org/geoserver/", "waterpoints_et", "biomass", 2024, 4, 22))

    def get_geo_polygon_name(self, workspace, user, password):
        """
        Retrieves the names and hrefs of polygons from the specified workspace in GeoServer.

        Args:
            workspace (str): The name of the workspace in GeoServer.
            user (str): The username for the GeoServer instance.
            password (str): The password for the GeoServer instance.

        Returns:
            pandas.DataFrame: A DataFrame containing the names and hrefs of the polygons, with columns 'polygon_name' and 'polygon_href'.
                             If no polygons are found or an error occurs, an empty DataFrame is returned.
        """

        if not user or not password:
            print("Error: Missing GeoServer credentials")
            return pd.DataFrame()

        try:
            url = f"{self.url_root}rest/workspaces/{workspace}/datastores.json"
            response = requests.get(url, auth=(user, password))
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return pd.DataFrame()

        if response.status_code == 401:
            print("Error: Unauthorized. Check your GeoServer credentials.")
            return pd.DataFrame()

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print("Error: Failed to decode the response as JSON")
            print(e)
            return pd.DataFrame()

        if 'dataStores' in data and 'dataStore' in data['dataStores']:
            try:
                polygons_list = data['dataStores']['dataStore']
                polygons_df = pd.DataFrame([{'polygon_name': pg['name'], 'polygon_href': pg['href']} for pg in polygons_list])
            except KeyError as e:
                print("Error: Missing key in data")
                print(e)
                return pd.DataFrame()
            return polygons_df

        return pd.DataFrame()

    # print(get_geo_polygon_name("https://geo.aclimate.org/geoserver/", "fc_cenaos_hn"))

    def get_geo_polygons(self, workspace, polygon_name):
        """
        Retrieves geo polygons from a GeoServer.

        Args:
            workspace (str): The name of the workspace in GeoServer.
            polygon_name (str): The name of the polygon to retrieve.

        Returns:
            GeoDataFrame or None: The retrieved geo polygons as a GeoDataFrame if successful, 
            None otherwise.
        """
        try:
            url = f"{self.url_root}/{workspace}/ows?service=WFS&request=GetFeature&version=2.0.1&typeNames={workspace}:{polygon_name}&outputFormat=application/json"
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return None

        if response.status_code == 200:
            try:
                sf_obj_geoserver = gpd.read_file(response.text)
                return sf_obj_geoserver
            except Exception as e:
                print("Error: Failed to read the response text as a file")
                print(e)
                return None

        else:
            exception_text = re.search(r'<ows:ExceptionText>(.*?)</ows:ExceptionText>', response.text)
            if exception_text:
                print(f"Error making the request. Status code: {response.status_code}\nMsg: {exception_text.group(1)}")
            else:
                print(f"Error making the request. Status code: {response.status_code}")
            return None
        
    # print(get_geo_polygons("https://geo.aclimate.org/geoserver/", "fc_cenaos_hn", "admin_levels"))