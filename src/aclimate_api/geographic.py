import requests
import json
import pandas as pd

def get_geographic_country(url_root):
    # Download data
    url = f"{url_root}Geographic/Country/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.DataFrame(data)
    return df

#print(get_geographic("https://webapi.aclimate.org/api/"))

def get_geographic(url_root, country_id):
    # Download data
    url = f"{url_root}Geographic/{country_id}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df_list = []
    
    for s in data:
        for m in s['municipalities']:
            for w in m['weather_stations']:
                df_list.append({
                    'country_id': s['country']['id'],
                    'country_iso2': s['country']['iso2'],
                    'country_name': s['country']['name'],
                    'state_id': s['id'],
                    'state_name': s['name'],
                    'municipality_id': m['id'],
                    'municipality_name': m['name'],
                    'ws_id': w['id'],
                    'ws_ext_id': w['ext_id'],
                    'ws_name': w['name'],
                    'ws_origin': w['origin'],
                    'ws_lat': w['latitude'],
                    'ws_lon': w['longitude']
                })

    df = pd.DataFrame(df_list)

    return df

#print(get_geographic("https://webapi.aclimate.org/api/", "636c0813e57f2e6ac61394e6"))

def get_geographic_crop(url_root, country_id):
    # Download data
    url = f"{url_root}Geographic/Crop/{country_id}/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df_list = []
    
    for cr in data:
        for s in cr['states']:
            for m in s['municipalities']:
                for w in m['weather_stations']:
                    df_list.append({
                        'crop_id': cr['id'],
                        'crop_name': cr['name'],
                        'country_iso2': s['country']['iso2'],
                        'country_name': s['country']['name'],
                        'state_id': s['id'],
                        'state_name': s['name'],
                        'municipality_id': m['id'],
                        'municipality_name': m['name'],
                        'ws_id': w['id'],
                        'ws_ext_id': w['ext_id'],
                        'ws_name': w['name'],
                        'ws_origin': w['origin'],
                        'ws_lat': w['latitude'],
                        'ws_lon': w['longitude']
                    })

    df = pd.DataFrame(df_list)
    return df

#print(get_geographic_crop("https://webapi.aclimate.org/api/", "61e59d829d5d2486e18d2ea8"))

def get_geographic_ws(url_root, country_id):
    # Download data
    url = f"{url_root}Geographic/{country_id}/WeatherStations/json"
    response = requests.get(url)
    data = json.loads(response.text)
    
    df = pd.DataFrame(data)
    return df

print(get_geographic_crop("https://webapi.aclimate.org/api/", "61e59d829d5d2486e18d2ea8"))