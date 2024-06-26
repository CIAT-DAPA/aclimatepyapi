# AClimate Py API

The AClimate Py API package is a comprehensive Python interface for accessing the AClimate Web API.
This package seamlessly integrates with Python, providing users with convenient access to a wide range of agro-climatic
forecasts offered by the AClimate platform.

- [Oficial website](https://www.aclimate.org).
- Source code [source code](https://github.com/CIAT-DAPA/aclimatepyapi/).
- Documentation of Web API and Dictionary of variable [documentation](https://docs.aclimate.org/en/latest/08-webapi.html).
- Depends **Python (>= 3.x)**
- Author [stevensotelo](https://github.com/stevensotelo), [Minotriz02](https://github.com/Minotriz02)

## Key Features

- Data Access: Access all relevant information from the AClimate platform, including accurate and up-to-date seasonal climate forecasts.

- User-Friendly: The package is designed with ease of use in mind, ensuring that users can effortlessly retrieve the information they need.

- Seamless Integration: Integrate AClimate data directly into R workflows, making it simple for users to incorporate climate and agroclimatic forecasts into their existing data analysis and decision-making processes

## Install

**Virtual environment creation**

Before installing the package first create a virtual environment to keep the package and dependencies only in the project to be used, to create the virtual environment in the terminal within the project run the following command

````bash
py -m venv [virtual_environment_name]
````

Then the virtual environment is started

````bash
[virtual_environment_name]\Scripts\activate.bat
````

Now you can continue with the installation of the package.

**Installation from GitHub**

The easiest way to install the package is from [Github repository](https://github.com/CIAT-DAPA/aclimatepyapi/) and using devtools.

````bash
pip install git+https://github.com/CIAT-DAPA/aclimatepyapi
````

If you want to download a specific version of orm you can do so by indicating the version tag (@v0.0.0) at the end of the install command

````bash
pip install git+https://github.com/CIAT-DAPA/aclimatepyapi@v0.2.0
````

## Remove

The easiest way to remove the package is:

```bash
pip uninstall aclimate-api
```

## How to use

The following list are recommendations which should be take into account when you try to use the package.

### Import library

Once you have installed the library, you should import it in order to get access to all functions

```python
from aclimate_api.[module_name] import [module_name]
```

### Url of the Web API and Geoserver

The first thing that you have to identify is the url which is located the Web API and the geoserver link. This parameter will be asked in all methods.

You can create a global variable with these url:

```python
URL_API = "https://webapi.aclimate.org/api/"
URL_GEOSERVER = "https://geo.aclimate.org/geoserver/"
```

## Functions

### Agronomy module

To use this module you need to import the module and create the object

```python
from aclimate_api.agronomy import Agronomy
agronomy = Agronomy(URL_API)
```
#### Get agronomy setup

The method **get_agronomy** allows to users get a list of cultivars and soils available into the AClimate platform.

```python
df = agronomy.get_agronomy()
print(df)
```

### Forecast module

To use this module you need to import the module and create the object

```python
from aclimate_api.forecast import Forecast
forecast = Forecast(URL_API)
```
#### Get climate forecast

The method **get_forecast_climate**, function which gets the forecast climate for a set of weather stations available into the AClimate platform.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
obj_f = forecast.get_forecast_climate(stations)
print(obj_f['probabilities'])
print(obj_f['performance'])
print(obj_f['scenarios'])
```
#### Get crop forecast

The method **get_forecast_crop**, function which gets the crop forecast for a set of weather stations available into the AClimate platform.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = forecast.get_forecast_crop(stations)
print(df)
```

#### Get forecast id

The method **get_forecast_information**, function which gets access primary forecast data for each month within a desired year.

```python
year = 2023
forecasts = forecast.get_forecast_information(year)
print(forecasts)
```

#### Get subseasonal forecast

The method **get_forecast_subseasonal**, function which gets information from the subseasonal forecast process, including probabilities and climatic scenarios.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations = ["63a3744005732d2a14260392","63a374ce05732d2a14260499"]
subseasonal_data = forecast.get_forecast_subseasonal(stations)
print(subseasonal_data)
```

#### Get previous climate forecast

The method **get_forecast_climate_previous**, function which gets the information obtained through the forecast process that is desired by means of the Id, the seasonal and subseasonal probabilities and the climatic scenarios.

You can find the ids of the weather stations in the method **get_geographic**
You can find the forecast id in the method **get_forecast_information**

```python
forecast_id = "657006544afb9646da8c6b78"
stations= ["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
obj_fp = forecast.get_forecast_climate_previous(forecast_id, stations)
print(obj_fp['probabilities'])
print(obj_fp['performance'])
print(obj_fp['scenarios'])
```

#### Get previous crop forecast

The method **get_forecast_crop_previous**, function which gets the crop forecast information for a specific forecast indicated in the parameters.

You can find the ids of the weather stations in the method **get_geographic**
You can find the forecast id in the method **get_forecast_information**

```python
forecast_id = "657006544afb9646da8c6b78"
stations= ["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = forecast.get_forecast_crop_previous(forecast_id, stations)
print(df)
```

#### Get forecast crop exceedance

The method **get_forecast_crop_exc**, function which gets the information obtained through of all forecast in the crop model process, yield data.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = forecast.get_forecast_crop_exc(stations)
print(df)
```

### Geographic Module

To use this module you need to import the module and create the object

```python
from aclimate_api.geographic import Geographic
geographic = Geographic(URL_API)
```

#### Get countries

The method **get_geographic_country** allows to users get a list of all countries.

```python
df = geographic.get_geographic_country()
print(df)
```

#### Get weather stations

The method **get_geographic** allows to users get a list of all weather stations available in a country.

You can find the ids of the countries in the method **get_geographic_country**

```python
id_country = "636c0813e57f2e6ac61394e6"
df = geographic.get_geographic(id_country)
print(df)
```

#### Get weather stations with crop information

The method **get_geographic** allows to users get a list of the states of the selected country with each of their municipalities and meteorological stations and for each meteorological station their productive ranges for each crop.

```python
country_id = "61e59d829d5d2486e18d2ea8"
df = geographic.get_geographic_crop(country_id)
print(df)
```

#### Get weather stations information

The method **get_geographic** allows to users get a list of detailed information weather stations, and crop-related details for a selected country.

```python
country_id = "61e59d829d5d2486e18d2ea8"
ws_list = geographic.get_geographic_ws(country_id)
print(ws_list)
```

### Historical Module

To use this module you need to import the module and create the object

```python
from aclimate_api.historical import Historical
historical = Historical(URL_API)
```

#### Get historical climatology

The method **get_historical_climatology**, function which gets the climatology of a selected weather station.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = historical.get_historical_climatology(stations)
print(df)
```

#### Get historical climate information

The method **get_historical_historicalclimatic**, function which gets the weather history of a selected weather station.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = historical.get_historical_historicalclimatic(stations)
print(df)
```

#### Get years with historical crop performance data

The method **get_historical_historicalyieldyears**, function which gets the years that contain historical crop performance data of the selected weather station.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
df = historical.get_historical_historicalyieldyears(stations)
print(df)
```

#### Get historical crop performance

The method **get_historical_historicalyield**, function which gets the yield data obtained through the crop model process.

You can find the ids of the weather stations in the method **get_geographic**

```python
stations=["58504f1a006cb93ed40eebe2","58504f1a006cb93ed40eebe3"]
years=["2022","2023"]
df = historical.get_historical_historicalyield(stations, years)
print(df)
```
### Geoserver Module

To use this module you need to import the module and create the object

```python
from aclimate_api.geoserver import Geoserver
geoserver = Geoserver(URL_GEOSERVER)
```

#### Get geoserver workspace

The method **get_geo_workspaces**, function which gets all the workspaces of the GeoServer. As arguments **user** is the username in geoserver and **password** is the geoserver password.

```python
obj_f = geoserver.get_geo_workspaces(user, password)
print(obj_f)
```

#### Get geoserver mosaic stores

The method **get_geo_mosaic_name**, function which gets all the mosaic stores of a specific workspace. As arguments **user** is the username in geoserver and **password** is the geoserver password.

You can find the workspace in the method **get_geo_workspaces**

```python
workspace = "climate_indices_pe"
obj_f = geoserver.get_geo_mosaic_name(workspace, user, password)
print(obj_f)
```

#### Get geoserver mosaics

The method **get_geo_mosaics**, function which gets the desired mosaic from the GeoServer.

You can find the workspace in the method **get_geo_workspaces**
You can find the mosaic_name in the method **get_geo_mosaic_name**

```python
workspace = "climate_indices_pe"
mosaic_name = "freq_rh80_t_20_25"
year = 2014
month = 5
day = 1
raster = geoserver.get_geo_mosaics(workspace, mosaic_name, year, month, day)
print(raster)
```

#### Get geoserver polygon stores

The method **get_geo_polygon_name**, function which gets all the polygon stores of a specific workspace. As arguments **user** is the username in geoserver and **password** is the geoserver password.

You can find the workspace in the method **get_geo_workspaces**

```python
workspace = "administrative"
obj_f = geoserver.get_geo_polygon_name(workspace, user, password)
print(obj_f)
```

#### Get geoserver shapefiles

The method **get_geo_polygons**, function which gets the desired shapefile from the GeoServer.

You can find the workspace in the method **get_geo_workspaces**
You can find the polygon_name in the method **get_geo_polygon_name**

```python
workspace = "administrative"
polygon_name = "ao_adm1"
shapefile = get_geo_polygons(workspace, polygon_name)
print(shapefile)
```


# Repository management:

### 3 main branches are managed.

- **main:**
  No changes should be made directly, since it is updated when pulling or pushing to the stage branch

- **stage:**
  The changes tested and ready to be sent to production must be sent to this branch, for their subsequent process of automatic tests, merge into master and creation of the release.

- **develop:**
  Branch where the development version of the project will be managed, normally changes will be sent to stage from this branch.

## Release:

    The release will be created automatically if changes are sent to stage, either by means of a pull request or a push.

    The release consists of versioning, which consists of the following format

    Release 0.0.0

- If you want to increase the last value, you must use the following tag within the commit a stage -> **#patch**

  - Current Release = Release 0.0.0

  - Release output = Release 0.0.1

- If you want to increase the value of the medium, you must use the following tag within the commit a stage -> **#minor**

  - Current Release = Release 0.0.0

  - Release output = Release 0.1.0

- If you want to increase the value of the medium, you must use the following tag within the commit a stage -> **#major**

  - Current Release = Release 0.0.0

  - Release output = Release 1.0.0

By **default** if a tag is not sent within the commit it will increment the last value, similar to the #patch tag.
