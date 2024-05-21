import requests
import json
import pandas as pd

class Historical:

    def __init__(self, url_root):
        self.url_root = url_root

    def get_historical_climatology(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}/Historical/Climatology/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)

        data_list = []
        for w in data:
            for md in w['monthly_data']:
                for wd in md['data']:
                    row_dict = {
                        'ws_id': w['weather_station'],
                        'month': md['month'],
                        'measure': wd['measure'],
                        'value': wd['value']
                    }
                    data_list.append(row_dict)

        df = pd.DataFrame(data_list)

        return df

    # print(get_historical_climatology("https://webapi.aclimate.org/api/", ['5a7e422057d7f316c8bc574e']))

    def get_historical_historicalclimatic(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}/Historical/HistoricalClimatic/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)

        data_list = []
        for w in data:
            for md in w['monthly_data']:
                for wd in md['data']:
                    row_dict = {
                        'ws_id': w['weather_station'],
                        'year': w['year'],
                        'month': md['month'],
                        'measure': wd['measure'],
                        'value': wd['value']
                    }
                    data_list.append(row_dict)

        df = pd.DataFrame(data_list)

        return df

    # print(get_historical_historicalclimatic("https://webapi.aclimate.org/api/", ['5a7e422057d7f316c8bc574e']))

    def get_historical_historicalyieldyears(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}/Historical/HistoricalYieldYears/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        df = pd.DataFrame({'year': data})
        return df

    # print(get_historical_historicalyieldyears("https://webapi.aclimate.org/api/", ['5a7e422057d7f316c8bc574e']))

    def get_historical_historicalyield(self, stations, years):
        ws = ",".join(stations)
        yearsSplit = ','.join(years)
        url = f"{self.url_root}/Historical/HistoricalYield/{ws}/{yearsSplit}/json"
        response = requests.get(url)
        data = json.loads(response.text)

        data_list = []
        for w in data:
            for wy in w['yield']:
                for y in wy['data']:
                    row_dict = {
                        'ws_id': w['weather_station'],
                        'cultivar': wy['cultivar'],
                        'soil': wy['soil'],
                        'start': wy['start'],
                        'end': wy['end'],
                        'measure': y['measure'],
                        'median': y['median'],
                        'avg': y['avg'],
                        'min': y['min'],
                        'max': y['max'],
                        'quar_1': y['quar_1'],
                        'quar_2': y['quar_2'],
                        'quar_3': y['quar_3'],
                        'conf_lower': y['conf_lower'],
                        'conf_upper': y['conf_upper'],
                        'sd': y['sd'],
                        'perc_5': y['perc_5'],
                        'perc_95': y['perc_95'],
                        'coef_var': y['coef_var']
                    }
                    data_list.append(row_dict)

        df = pd.DataFrame(data_list)

        return df

    # print(get_historical_historicalyield("https://webapi.aclimate.org/api/", ['5a7e422057d7f316c8bc574e'], ['2020', '2021']))