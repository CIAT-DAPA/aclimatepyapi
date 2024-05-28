import requests
import json
import pandas as pd

class Forecast:

    def __init__(self, url_root):
        self.url_root = url_root
        
    def get_forecast_climate(self, stations):
        """
        Retrieves the forecast climate data for the given weather stations.

        Args:
            stations (list): A list of weather station IDs.

        Returns:
            dict: A dictionary containing the forecast climate data, including probabilities,
                    performance, and scenarios. The keys of the dictionary are 'probabilities',
                    'performance', and 'scenarios', and the values are pandas DataFrames.

        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/Climate/{ws}/true/json"
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
        
        df_prob_list = []
        df_perf_list = []
        df_scen_list = []
        try:
            for w in data['climate']:
                for wd in w['data']:
                    for p in wd['probabilities']:
                        if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()):
                            df = pd.DataFrame(p, index=[0])
                        else:
                            df = pd.DataFrame(p)
                        df = df.assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month'])
                        df_prob_list.append(df)

                for p in w['performance']:
                    if isinstance(p, dict) and all(isinstance(v, (int, float, str)) for v in p.values()):
                        df = pd.DataFrame(p, index=[0])
                    else:
                        df = pd.DataFrame(p)
                    df_perf_list.append(df)

            for w in data['scenario']:
                for wm in w['monthly_data']:
                    for d in wm['data']:
                        if isinstance(d, dict) and all(isinstance(v, (int, float, str)) for v in d.values()):
                            df = pd.DataFrame(d, index=[0])
                        else:
                            df = pd.DataFrame(d)
                        df = df.assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month'])
                        df_scen_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df_prob = pd.concat(df_prob_list, ignore_index=True)
        df_perf = pd.concat(df_perf_list, ignore_index=True)
        df_scen = pd.concat(df_scen_list, ignore_index=True)
        forecast_climate = {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

        return forecast_climate

    # print(get_forecast_climate("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))
    
    def get_forecast_crop(self, stations):
        """
        Retrieves the forecast yield data for the specified weather stations.

        Args:
            stations (list): A list of weather station IDs.

        Returns:
            pandas.DataFrame: A DataFrame containing the forecast yield data for the specified weather stations.
        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/Yield/{ws}/json"
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

        df_yield_list = []
        try:
            for w in data.get('yield', []):
                for wy in w.get('yield', []):
                    for y in wy.get('data', []):
                        if isinstance(y, dict) and all(isinstance(v, (int, float, str)) for v in y.values()):
                            df = pd.DataFrame(y, index=[0])
                        else:
                            df = pd.DataFrame(y)
                        df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                        df_yield_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df = pd.concat(df_yield_list, ignore_index=True) if df_yield_list else pd.DataFrame()
        return df

    # print(get_forecast_crop("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_information(self, year):
        """
        Retrieves forecast information for a given year.

        Args:
            year (int): The year for which to retrieve the forecast information.

        Returns:
            pandas.DataFrame: A DataFrame containing the forecast information, including columns for 'id', 'start', 'end', and 'confidence'.
        """
        try:
            url = f"{self.url_root}Forecast/Log/{year}/json"
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

        df_list = []
        try:
            for c in data:
                df = pd.DataFrame({
                    'id': c['id'], 
                    'start': c['start'], 
                    'end': c['end'], 
                    'confidence': c['confindece']
                }, index=[0])
                df_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df = pd.concat(df_list, ignore_index=True)
        return df

    # print(get_forecast_information("https://webapi.aclimate.org/api/", 2021))

    def get_forecast_subseasonal(self, stations):
        """
        Retrieves the subseasonal forecast data for the given weather stations.

        Args:
            stations (list): A list of weather station IDs.

        Returns:
            pandas.DataFrame: A DataFrame containing the subseasonal forecast data.
                The DataFrame has the following columns:
                - weather_station: The ID of the weather station.
                - year: The year of the forecast.
                - month: The month of the forecast.
                - week: The week of the forecast.
                - measure: The measure of the forecast.
                - lower: The lower bound of the forecast.
                - normal: The normal value of the forecast.
                - upper: The upper bound of the forecast.

                If no subseasonal forecast data is available, an empty DataFrame is returned.
        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/SubseasonalWS/{ws}/json"
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

        if not data.get('subseasonal'):
            return pd.DataFrame()

        data_list = []
        try:
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
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        if not data_list:
            return pd.DataFrame()

        df = pd.DataFrame(data_list)
        return df
    
    # print(get_forecast_subseasonal("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_climate_previous(self, forecast, stations):
        """
        Retrieves the forecast climate data for previous periods.

        Args:
            forecast (str): The forecast identifier.
            stations (list): A list of weather station IDs.

        Returns:
            dict: A dictionary containing the forecast climate data for previous periods.
                The dictionary has the following keys:
                - 'probabilities': A pandas DataFrame containing the probability data.
                - 'performance': A pandas DataFrame containing the performance data.
                - 'scenarios': A pandas DataFrame containing the scenario data.
        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/ClimatePrevious/{forecast}/{ws}/true/json"
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

        df_prob_list = []
        df_perf_list = []
        df_scen_list = []

        try:
            for w in data['climate']:
                for wd in w['data']:
                    for p in wd['probabilities']:
                        if isinstance(p, dict) and all(isinstance(value, (int, float, str)) for value in p.values()):
                            df = pd.DataFrame(p, index=[0])
                        else:
                            df = pd.DataFrame(p)
                        df = df.assign(ws_id=w['weather_station'], year=wd['year'], month=wd['month'])
                        df_prob_list.append(df)

                for p in w['performance']:
                    if isinstance(p, dict) and all(isinstance(value, (int, float, str)) for value in p.values()):
                        df = pd.DataFrame(p, index=[0])
                    else:
                        df = pd.DataFrame(p)
                    df = df.assign(ws_id=w['weather_station'], year=p['year'], month=p['month'])
                    df_perf_list.append(df)

            for w in data['scenario']:
                for wm in w['monthly_data']:
                    for d in wm['data']:
                        if isinstance(d, dict) and all(isinstance(value, (int, float, str)) for value in d.values()):
                            df = pd.DataFrame(d, index=[0])
                        else:
                            df = pd.DataFrame(d)
                        df = df.assign(ws_id=w['weather_station'], scenario=w['name'], year=w['year'], month=wm['month'])
                        df_scen_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df_prob = pd.concat(df_prob_list, ignore_index=True)
        df_perf = pd.concat(df_perf_list, ignore_index=True)
        df_scen = pd.concat(df_scen_list, ignore_index=True)

        forecast_climate_previous = {'probabilities': df_prob, 'performance': df_perf, 'scenarios': df_scen}

        return forecast_climate_previous

    # print(get_forecast_climate_previous("https://webapi.aclimate.org/api/", "602d1da7a1c81c22b08683b5", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_crop_previous(self, forecast, stations):
        """
        Retrieves the previous yield forecast for a given forecast and list of weather stations.

        Args:
            forecast (str): The forecast identifier.
            stations (list): A list of weather station identifiers.

        Returns:
            pandas.DataFrame: A DataFrame containing the forecasted yield data for the specified forecast and weather stations.
        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/YieldPrevious/{forecast}/{ws}/json"
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

        df_list = []
        try:
            for w in data.get('yield', []):
                for wy in w.get('yield', []):
                    for y in wy.get('data', []):
                        if isinstance(y, dict) and all(isinstance(value, (int, float, str)) for value in y.values()):
                            df = pd.DataFrame(y, index=[0])
                        else:
                            df = pd.DataFrame(y)
                        df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                        df_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        if df_list:
            df = pd.concat(df_list, ignore_index=True)
        else:
            df = pd.DataFrame()

        return df

    # print(get_forecast_crop_previous("https://webapi.aclimate.org/api/", "602d1da7a1c81c22b08683b5", ["5a7e422057d7f316c8bc574e"]))

    def get_forecast_crop_exc(self, stations):  
        """
        Retrieves the forecast crop exceedance data for the given weather stations.

        Args:
            stations (list): A list of weather station IDs.

        Returns:
            pandas.DataFrame: A DataFrame containing the forecast crop exceedance data.
        """
        try:
            ws = ",".join(stations)
            url = f"{self.url_root}Forecast/YieldExceedance/{ws}/json"
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

        df_yield_list = []
        try:
            for w in data.get('yield', []):
                for wy in w.get('yield', []):
                    for y in wy.get('data', []):
                        if isinstance(y, dict) and all(isinstance(v, (int, float, str)) for v in y.values()):
                            df = pd.DataFrame(y, index=[0])
                        else:
                            df = pd.DataFrame(y)
                        df = df.assign(ws_id=w['weather_station'], cultivar=wy['cultivar'], soil=wy['soil'], start=wy['start'], end=wy['end'])
                        df_yield_list.append(df)
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df = pd.concat(df_yield_list, ignore_index=True) if df_yield_list else pd.DataFrame()

        return df

    # print(get_forecast_crop_exc("https://webapi.aclimate.org/api/", ["5a7e422057d7f316c8bc574e"]))
