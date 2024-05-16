from geographic import Geographic
from forecast import Forecast

def main():
    g = Geographic("https://webapi.aclimate.org/api/")
    print(g.get_geographic("636c0813e57f2e6ac61394e6"))
    f = Forecast("https://webapi.aclimate.org/api/")
    print(f.get_forecast_climate(["5a7e422057d7f316c8bc574e"]))

if __name__ == "__main__":
    main()