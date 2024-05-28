import requests
import json
import pandas as pd

class Geographic:
    def __init__(self, url_root):
        self.url_root = url_root

    def get_geographic_country(self):
        """
        Retrieves geographic country data from the API.

        Returns:
            pandas.DataFrame: A DataFrame containing the geographic country data.
        """
        try:
            url = f"{self.url_root}Geographic/Country/json"
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

        try:
            df = pd.DataFrame(data)
        except ValueError as e:
            print("Error: Failed to convert data to DataFrame")
            print(e)
            return None

        return df

    #print(get_geographic("https://webapi.aclimate.org/api/"))

    def get_geographic(self, country_id):
        """
        Retrieves geographic data for a given country ID.

        Parameters:
        - country_id (str): The ID of the country for which to retrieve geographic data.

        Returns:
        - df (pandas.DataFrame): A DataFrame containing the retrieved geographic data.
        """
        try:
            url = f"{self.url_root}Geographic/{country_id}/json"
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
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df = pd.DataFrame(df_list)

        return df

    #print(get_geographic("https://webapi.aclimate.org/api/", "636c0813e57f2e6ac61394e6"))

    def get_geographic_crop(self, country_id):
        """
        Retrieves geographic crop data for a given country.

        Args:
            country_id (str): The ID of the country for which to retrieve crop data.

        Returns:
            pandas.DataFrame: A DataFrame containing the geographic crop data.
        """
        try:
            url = f"{self.url_root}Geographic/Crop/{country_id}/json"
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
        except KeyError as e:
            print("Error: Missing key in data")
            print(e)
            return None

        df = pd.DataFrame(df_list)

        return df

    #print(get_geographic_crop("https://webapi.aclimate.org/api/", "61e59d829d5d2486e18d2ea8"))

    def get_geographic_ws(self, country_id):
        """
        Retrieves weather stations data for a specific country.

        Parameters:
        country_id (str): The ID of the country for which to retrieve weather stations data.

        Returns:
        pandas.DataFrame: A DataFrame containing the weather stations data.
        """
        try:
            url = f"{self.url_root}Geographic/{country_id}/WeatherStations/json"
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

        try:
            df = pd.DataFrame(data)
        except ValueError as e:
            print("Error: Failed to convert data to DataFrame")
            print(e)
            return None

        return df

    # print(get_geographic_crop("https://webapi.aclimate.org/api/", "61e59d829d5d2486e18d2ea8"))