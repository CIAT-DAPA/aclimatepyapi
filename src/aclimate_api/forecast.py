import requests
import json
import pandas as pd

class Forecast:

    def __init__(self, url_root):
        self.url_root = url_root
        
    def get_forecast_climate(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}Forecast/Climate/{ws}/true/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_prob_list = []
        for w in data['climate']:
            for wd in w['data']:
                for p in wd['probabilities']:
                    if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()):
                        df = pd.DataFrame(p, index=[0])
                    else:
                        df = pd.DataFrame(p)
                    df = df.assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month'])
                    df_prob_list.append(df)
        df_prob = pd.concat(df_prob_list, ignore_index=True)

        df_perf_list = []
        for w in data['climate']:
            for p in w['performance']:
                if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()):
                    df = pd.DataFrame(p, index=[0])
                else:
                    df = pd.DataFrame(p)
                df_perf_list.append(df)
        df_perf = pd.concat(df_perf_list, ignore_index=True)

        df_scen_list = []
        for w in data['scenario']:
            for wm in w['monthly_data']:
                for d in wm['data']:
                    if isinstance(d, dict) and all(isinstance(v, (int, float, str)) for v in d.values()):
                        df = pd.DataFrame(d, index=[0])
                    else:
                        df = pd.DataFrame(d)
                    df = df.assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month'])
                    df_scen_list.append(df)
        df_scen = pd.concat(df_scen_list, ignore_index=True)
        forecast_climate = {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

        return forecast_climate

    # print(get_forecast_climate("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_crop(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}Forecast/Yield/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_yield_list = []
        for w in data.get('yield', []):
            for wy in w.get('yield', []):
                for y in wy.get('data', []):
                    if isinstance(y, dict) and all(isinstance(v, (int, float, str)) for v in y.values()):
                        df = pd.DataFrame(y, index=[0])
                    else:
                        df = pd.DataFrame(y)
                    df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                    df_yield_list.append(df)
        df = pd.concat(df_yield_list, ignore_index=True) if df_yield_list else pd.DataFrame()
        return df

    # print(get_forecast_crop("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_information(self, year):
        url = f"{self.url_root}Forecast/Log/{year}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_list = []
        for c in data:
            df = pd.DataFrame({
                'id': c['id'], 
                'start': c['start'], 
                'end': c['end'], 
                'confindece': c['confindece']
            }, index=[0])
            df_list.append(df)
        df = pd.concat(df_list, ignore_index=True)
        
        return df

    # print(get_forecast_information("https://webapi.aclimate.org/api/", 2021))

    def get_forecast_subseasonal(url_root, stations):
        ws = ",".join(stations)
        url = f"{url_root}Forecast/SubseasonalWS/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)

        if not data.get('subseasonal'):
            return pd.DataFrame()  

        data_list = []
        for x in data['subseasonal']:
            if not x.get('data'):
                continue  
            for y in x['data']:
                if not y.get('probabilities'):
                    continue  
                for z in y['probabilities']:
                    data_dict = {
                        'weather_station': x['weather_station'],
                        'year': y['year'],
                        'month': y['month'],
                        'week': y['week'],
                        'measure': z['measure'],
                        'lower': z['lower'],
                        'normal': z['normal'],
                        'upper': z['upper']
                    }
                    data_list.append(data_dict)

        if not data_list:
            return pd.DataFrame()  

        df = pd.DataFrame(data_list)
        return df
    
    # print(get_forecast_subseasonal("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_climate_previous(self, forecast, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}Forecast/ClimatePrevious/{forecast}/{ws}/true/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_prob_list = []
        for w in data['climate']:
            for wd in w['data']:
                for p in wd['probabilities']:
                    if isinstance(p, dict) and all(isinstance(value, (int, float, str)) for value in p.values()):
                        df = pd.DataFrame(p, index=[0])
                    else:
                        df = pd.DataFrame(p)
                    df = df.assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month'])
                    df_prob_list.append(df)
        df_prob = pd.concat(df_prob_list, ignore_index=True)

        df_perf_list = []
        for w in data['climate']:
            for p in w['performance']:
                if isinstance(p, dict) and all(isinstance(value, (int, float, str)) for value in p.values()):
                    df = pd.DataFrame(p, index=[0])
                else:
                    df = pd.DataFrame(p)
                df = df.assign(ws_id=w['weather_station'], year=p['year'], month=p['month'])
                df_perf_list.append(df)
        df_perf = pd.concat(df_perf_list, ignore_index=True)

        df_scen_list = []
        for w in data['scenario']:
            for wm in w['monthly_data']:
                for d in wm['data']:
                    if isinstance(d, dict) and all(isinstance(value, (int, float, str)) for value in d.values()):
                        df = pd.DataFrame(d, index=[0])
                    else:
                        df = pd.DataFrame(d)
                    df = df.assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month'])
                    df_scen_list.append(df)
        df_scen = pd.concat(df_scen_list, ignore_index=True)

        forecast_climate_previous = {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

        return forecast_climate_previous

    # print(get_forecast_climate_previous("https://webapi.aclimate.org/api/", "602d1da7a1c81c22b08683b5", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_crop_previous(self, forecast, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}Forecast/YieldPrevious/{forecast}/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_list = []
        for w in data.get('yield', []):
            for wy in w.get('yield', []):
                for y in wy.get('data', []):
                    if isinstance(y, dict) and all(isinstance(value, (int, float, str)) for value in y.values()):
                        df = pd.DataFrame(y, index=[0])
                    else:
                        df = pd.DataFrame(y)
                    df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                    df_list.append(df)
        if df_list:
            df = pd.concat(df_list, ignore_index=True)
        else:
            df = pd.DataFrame()

        return df

    # print(get_forecast_crop_previous("https://webapi.aclimate.org/api/", "602d1da7a1c81c22b08683b5", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_crop_exc(self, stations):
        ws = ",".join(stations)
        url = f"{self.url_root}Forecast/YieldExceedance/{ws}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        
        df_yield_list = []
        for w in data.get('yield', []):
            for wy in w.get('yield', []):
                for y in wy.get('data', []):
                    if isinstance(y, dict) and all(isinstance(v, (int, float, str)) for v in y.values()):
                        df = pd.DataFrame(y, index=[0])
                    else:
                        df = pd.DataFrame(y)
                    df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                    df_yield_list.append(df)
        df = pd.concat(df_yield_list, ignore_index=True) if df_yield_list else pd.DataFrame()
        
        return df

    # print(get_forecast_crop_exc("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))
