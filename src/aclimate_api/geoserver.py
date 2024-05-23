import requests
import pandas as pd
import rasterio
from rasterio.io import MemoryFile
import json
import re

def get_geo_workspaces(url_root):

    with open("../../geo_config.txt", "r") as f:
        credentials = dict(line.strip().split('=') for line in f.readlines())
    
    url = f"{url_root}/rest/workspaces.json"

    response = requests.get(url, auth=(credentials['GEOSERVER_USER'], credentials['GEOSERVER_PASSWORD']))
    
    data = json.loads(response.text)
    workspaces_list = data['workspaces']['workspace']
    workspace_df = pd.DataFrame([{'workspace_name': ws['name'], 'workspace_href': ws['href']} for ws in workspaces_list])
    return workspace_df

# print(get_geo_workspaces("https://geo.aclimate.org/geoserver/"))

def get_geo_mosaic_name(url_root, workspace):    
    with open("../../geo_config.txt", "r") as f:
        credentials = dict(line.strip().split('=') for line in f.readlines())
    
    url = f"{url_root}/rest/workspaces/{workspace}/coveragestores.json"

    response = requests.get(url, auth=(credentials['GEOSERVER_USER'], credentials['GEOSERVER_PASSWORD']))
    
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'coverageStores' in data and 'coverageStore' in data['coverageStores']:
            mosaics_list = data['coverageStores']['coverageStore']
            mosaics_df = pd.DataFrame([{'mosaic_name': ms['name'], 'mosaic_href': ms['href']} for ms in mosaics_list])
            return mosaics_df
    return pd.DataFrame()

# print(get_geo_mosaic_name("https://geo.aclimate.org/geoserver/", "waterpoints_et"))

def get_geo_mosaics(url_root, workspace, mosaic_name, year, month=1, day=1):
    
    url = f"{url_root}/{workspace}/ows?service=WCS&request=GetCoverage&version=2.0.1&coverageId={mosaic_name}&format=image/geotiff&subset=Time(\"{year}-{month:02d}-{day:02d}T00:00:00.000Z\")"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        with MemoryFile(response.content) as memfile:
            with memfile.open() as dataset:
                raster_data = dataset.read(1)
                return raster_data
    else:
        exception_text = re.search(r'<ows:ExceptionText>(.*?)</ows:ExceptionText>', response.text)
        if exception_text:
            print(f"Error making the request. Status code: {response.status_code}\nMsg: {exception_text.group(1)}")
        else:
            print(f"Error making the request. Status code: {response.status_code}")
        return None

print(get_geo_mosaics("https://geo.aclimate.org/geoserver/waterpoints_et", "waterpoints_et", "biomass", 2024,4,24))