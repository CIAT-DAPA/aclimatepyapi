from geographic import Geographic
from forecast import Forecast
from agronomy import Agronomy
from historical import Historical
from geoserver import Geoserver

def main():
    g = Geographic("https://webapi.aclimate.org/api/")
    # print(g.get_geographic_ws("61e59d829d5d2486e18d2ea8"))
    f = Forecast("https://webapi.aclimate.org/api/")
    # print(f.get_forecast_crop_exc(["5a7e422057d7f316c8bc574e"]))
    a = Agronomy("https://webapi.aclimate.org/api/")
    # print(a.get_agronomy())
    h = Historical("https://webapi.aclimate.org/api/")
    # print(h.get_historical_climatology(["5a7e422057d7f316c8bc574e"]))
    gs = Geoserver("https://geo.aclimate.org/geoserver/")
    # print(gs.get_geo_polygon_name("fc_cenaos_hn"))

if __name__ == "__main__":
    main()