import requests
import json
import pandas as pd

def get_forecast_climate(url_root, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/Climate/{ws}/true/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df_prob = pd.concat([pd.concat([pd.DataFrame(p, index=[0]) if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()) else pd.DataFrame(p) for p in wd['probabilities']], ignore_index=True).assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month']) for w in data['climate'] for wd in w['data']], ignore_index=True) 
    df_perf = pd.concat([pd.DataFrame(p, index=[0]) if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()) else pd.DataFrame(p) for w in data['climate'] for p in w['performance']], ignore_index=True) 
    df_scen = pd.concat([pd.concat([pd.concat([pd.DataFrame(d, index=[0]) if isinstance(d, dict) and all(isinstance(v, (int, float, str)) for v in d.values()) else pd.DataFrame(d) for d in wm['data']], ignore_index=True).assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month']) for wm in w['monthly_data']], ignore_index=True) for w in data['scenario']], ignore_index=True)
    
    forecast_climate = {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

    return forecast_climate

# print(get_forecast_climate("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

def get_forecast_crop(url_root, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/Yield/{ws}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.concat([pd.concat([pd.concat([pd.DataFrame(y, index=[0]) if isinstance(y, dict) and all(isinstance(v, (int, float, str)) for v in y.values()) else pd.DataFrame(y) for y in wy['data']], ignore_index=True).assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end']) for wy in w['yield']], ignore_index=True) for w in data['yield']], ignore_index=True)

    return df

# print(get_forecast_crop("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

def get_forecast_information(url_root, year):
    url = f"{url_root}Forecast/Log/{year}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.concat([pd.DataFrame({'id': c['id'], 'start': c['start'], 'end': c['end'], 'confindece': c['confindece']}, index=[0]) for c in data], ignore_index=True)
    
    return df

# print(get_forecast_information("https://webapi.aclimate.org/api/", 2021))

def get_forecast_subseasonal(url_root, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/SubseasonalWS/{ws}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    if data['subseasonal']:
        df = pd.concat([pd.concat([pd.concat([pd.DataFrame({'weather_station': x['weather_station'], 'year': y['year'], 'month': y['month'], 'week': y['week']}, index=[0]).assign(**{z['measure']: z['value'] for z in y['probabilities']}) for y in x['data']], ignore_index=True) if x['data'] else pd.DataFrame() for x in data['subseasonal']], ignore_index=True) for x in data['subseasonal']], ignore_index=True)
    else:
        df = pd.DataFrame()

    return df

print(get_forecast_subseasonal("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

def get_forecast_climate_previous(url_root, forecast, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/ClimatePrevious/{forecast}/{ws}/true/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df_prob = pd.concat([pd.concat([pd.concat([pd.DataFrame(p) for p in wd['probabilities']], ignore_index=True).assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month']) for wd in w['data']], ignore_index=True) for w in data['climate']], ignore_index=True)
    
    df_perf = pd.concat([pd.DataFrame(p).assign(ws_id=w['weather_station'], year=p['year'], month=p['month']) for w in data['climate'] for p in w['performance']], ignore_index=True)
    
    df_scen = pd.concat([pd.concat([pd.concat([pd.DataFrame(d) for d in wm['data']], ignore_index=True).assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month']) for wm in w['monthly_data']], ignore_index=True) for w in data['scenario']], ignore_index=True)
    
    return {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

def get_forecast_crop_previous(url_root, forecast, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/YieldPrevious/{forecast}/{ws}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.concat([pd.concat([pd.concat([pd.DataFrame(y) for y in wy['data']], ignore_index=True).assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end']) for wy in w['yield']], ignore_index=True) for w in data['yield']], ignore_index=True)
    
    return df

def get_forecast_crop_exc(url_root, stations):
    ws = ",".join(stations)
    url = f"{url_root}Forecast/YieldExceedance/{ws}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.concat([pd.concat([pd.concat([pd.DataFrame(y) for y in wy['data']], ignore_index=True).assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end']) for wy in w['yield']], ignore_index=True) for w in data['yield']], ignore_index=True)
    
    return df
