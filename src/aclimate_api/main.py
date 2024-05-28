import os
from geographic import Geographic
from forecast import Forecast
from agronomy import Agronomy
from historical import Historical
from geoserver import Geoserver

def main():
    g = Geographic("https://webapi.aclimate.org/api/")
    # print(g.get_geographic("636c0813e57f2e6ac61394e6"))
    f = Forecast("https://webapi.aclimate.org/api/")
    # print(f.get_forecast_climate(["5a7e422057d7f316c8bc574e"]))
    a = Agronomy("https://webapi.aclimate.org/api/")
    # print(a.get_agronomy())
    h = Historical("https://webapi.aclimate.org/api/")
    # print(h.get_historical_climatology(["5a7e422057d7f316c8bc574e"]))
    gs = Geoserver("https://geo.aclimate.org/geoserver/")
    # print(gs.get_geo_workspaces())

if __name__ == "__main__":
    main()