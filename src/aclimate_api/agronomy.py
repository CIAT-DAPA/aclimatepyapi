import requests
import json
import pandas as pd

class Agronomy:

    def __init__(self, url_root):
        self.url_root = url_root

    """
    Retrieves agronomy data from the API.

    Returns:
        dict: A dictionary containing two DataFrames: 'cultivars' and 'soils'.
            The 'cultivars' DataFrame contains information about different cultivars,
            including crop ID, crop name, cultivar ID, cultivar name, rainfed status,
            and national status.
            The 'soils' DataFrame contains information about different soils,
            including crop ID, crop name, soil ID, and soil name.
    """
    def get_agronomy(self):
        try:
            url = f"{self.url_root}Agronomic/true/json"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the GET request failed
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve data from {url}")
            print(e)
            return None

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print("Error: Failed to decode the response as JSON")
            print(e)
            return None

        cultivars_data = []
        soils_data = []
        try:
            for crop in data:
                for cultivar in crop['cultivars']:
                    cultivars_data.append({
                        'crop_id': crop['cp_id'],
                        'crop_name': crop['cp_name'],
                        'cultivar_id': cultivar['id'],
                        'cultivar_name': cultivar['name'],
                        'cultivar_rainfed': cultivar['rainfed'],
                        'cultivar_national': cultivar['national']
                    })

                for soil in crop['soils']:
                    soils_data.append({
                        'crop_id': crop['cp_id'],
                        'crop_name': crop['cp_name'],
                        'soil_id': soil['id'],
                        'soil_name': soil['name']
                    })
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        agronomy = {'cultivars': pd.DataFrame(cultivars_data), 'soils': pd.DataFrame(soils_data)}
        return agronomy

# print(get_agronomy("https://webapi.aclimate.org/api/"))