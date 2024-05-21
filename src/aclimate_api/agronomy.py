import requests
import json
import pandas as pd


class Agronomy:

    def __init__(self, url_root):
        self.url_root = url_root

    def get_agronomy(self):
        url = f"{self.url_root}Agronomic/true/json"
        response = requests.get(url)
        data = json.loads(response.text)

        cultivars_data = []
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

        soils_data = []
        for crop in data:
            for soil in crop['soils']:
                soils_data.append({
                    'crop_id': crop['cp_id'],
                    'crop_name': crop['cp_name'],
                    'soil_id': soil['id'],
                    'soil_name': soil['name']
                })

        agronomy = {'cultivars': pd.DataFrame(cultivars_data), 'soils': pd.DataFrame(soils_data)}
        return agronomy

# print(get_agronomy("https://webapi.aclimate.org/api/"))