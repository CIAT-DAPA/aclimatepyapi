# Datos de países
geographic_country_mock_data = '''
[
    {
        "id": "61e59d829d5d2486e18d2ea8",
        "iso2": "CO",
        "name": "Colombia"
    },
    {
        "id": "61e59d829d5d2486e18d2ea9",
        "iso2": "ET",
        "name": "Ethiopia"
    },
    {
        "id": "62a739250dd05810f0e2938d",
        "iso2": "AO",
        "name": "Angola"
    },
    {
        "id": "636c0813e57f2e6ac61394e6",
        "iso2": "GT",
        "name": "Guatemala"
    },
    {
        "id": "641c820e4fb2a6438cc670e7",
        "iso2": "MW",
        "name": "Malawi"
    },
    {
        "id": "641c82214fb2a6438cc670eb",
        "iso2": "TZ",
        "name": "Tanzania"
    },
    {
        "id": "641c82304fb2a6438cc670ee",
        "iso2": "ZM",
        "name": "Zambia"
    },
    {
        "id": "6438525c843fb30d41311d25",
        "iso2": "PE",
        "name": "Peru"
    },
    {
        "id": "651437a78a8437279ea6ca2c",
        "iso2": "NI",
        "name": "Nicaragua"
    }
]
'''

# Datos geográficos
geographic_mock_data = '''
[
  {
    "id": "58504314333cb94a800f8098",
    "name": "Casanare",
    "country": {
      "id": "61e59d829d5d2486e18d2ea8",
      "iso2": "CO",
      "name": "Colombia"
    },
    "municipalities": [
      {
        "id": "58504f1a006cb93ed40eebd9",
        "name": "Aguazul",
        "weather_stations": [
          {
            "id": "58504f1a006cb93ed40eebe2",
            "ext_id": "35195030",
            "name": "Aguazul",
            "origin": "IDEAM",
            "latitude": 5.179333333,
            "longitude": -72.55088889,
            "ranges": [
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bajo",
                "lower": 0,
                "upper": 3000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Regular",
                "lower": 3001,
                "upper": 5000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Normal",
                "lower": 5001,
                "upper": 5500
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bueno",
                "lower": 5501,
                "upper": 6000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Excelente",
                "lower": 6001,
                "upper": 99999
              }
            ]
          }
        ]
      },
      {
        "id": "58504f1a006cb93ed40eebda",
        "name": "Yopal",
        "weather_stations": [
          {
            "id": "58504f1a006cb93ed40eebe3",
            "ext_id": "35215010",
            "name": "Aeropuerto Yopal",
            "origin": "IDEAM",
            "latitude": 5.320444444,
            "longitude": -72.3875,
            "ranges": [
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bajo",
                "lower": 0,
                "upper": 1500
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Regular",
                "lower": 1501,
                "upper": 3000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Normal",
                "lower": 3001,
                "upper": 4500
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bueno",
                "lower": 4501,
                "upper": 6000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Excelente",
                "lower": 6001,
                "upper": 99999
              }
            ]
          }
        ]
      },
      {
        "id": "5a7e416457d7f316c8bc5747",
        "name": "Orocue",
        "weather_stations": [
          {
            "id": "5a7e422057d7f316c8bc574e",
            "ext_id": "35225020",
            "name": "Modulos",
            "origin": "IDEAM",
            "latitude": 4.910472,
            "longitude": -71.433056,
            "ranges": [
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bajo",
                "lower": 0,
                "upper": 3000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Regular",
                "lower": 3001,
                "upper": 5000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Normal",
                "lower": 5001,
                "upper": 5500
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Bueno",
                "lower": 5501,
                "upper": 6000
              },
              {
                "crop_id": "585051c4c290272c481111a7",
                "crop_name": "Arroz",
                "label": "Excelente",
                "lower": 6001,
                "upper": 99999
              }
            ]
          }
        ]
      }
    ]
  }
]
'''

# Datos de estaciones meteorológicas
geographic_ws_mock_data = '''
[
    {
        "id": "64385742843fb30d41311d5a",
        "ext_id": "pe_00001",
        "name": "San Martin",
        "origin": "PISCO & ERA-5",
        "latitude": -6.517,
        "longitude": -76.73805556,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d5b",
        "ext_id": "pe_00002",
        "name": "Bellavista",
        "origin": "PISCO & ERA-5",
        "latitude": -7.055166667,
        "longitude": -76.55836111,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d5c",
        "ext_id": "pe_00003",
        "name": "Alto Biavo 1",
        "origin": "PISCO & ERA-5",
        "latitude": -7.2549686,
        "longitude": -76.47778469,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d61",
        "ext_id": "pe_00008",
        "name": "Alto Biavo 2",
        "origin": "PISCO & ERA-5",
        "latitude": -7.407111111,
        "longitude": -76.41388889,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d65",
        "ext_id": "pe_00012",
        "name": "Bajo Biavo 1",
        "origin": "PISCO & ERA-5",
        "latitude": -7.16319,
        "longitude": -76.49275,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d6a",
        "ext_id": "pe_00017",
        "name": "Bajo Biavo 2",
        "origin": "PISCO & ERA-5",
        "latitude": -7.096277778,
        "longitude": -76.47233333,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d75",
        "ext_id": "pe_00028",
        "name": "San Pablo",
        "origin": "PISCO & ERA-5",
        "latitude": -6.809555556,
        "longitude": -76.57625,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d5d",
        "ext_id": "pe_00004",
        "name": "Campanilla",
        "origin": "PISCO & ERA-5",
        "latitude": -7.484344444,
        "longitude": -76.65311111,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d63",
        "ext_id": "pe_00010",
        "name": "Juanjui",
        "origin": "PISCO & ERA-5",
        "latitude": -7.26871,
        "longitude": -76.73701,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d6c",
        "ext_id": "pe_00019",
        "name": "Pachiza",
        "origin": "PISCO & ERA-5",
        "latitude": -7.293222222,
        "longitude": -76.77091667,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d5e",
        "ext_id": "pe_00005",
        "name": "Chazuta",
        "origin": "PISCO & ERA-5",
        "latitude": -6.569003,
        "longitude": -76.1138026,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d5f",
        "ext_id": "pe_00006",
        "name": "Morales",
        "origin": "PISCO & ERA-5",
        "latitude": -6.67537,
        "longitude": -76.07798611,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d66",
        "ext_id": "pe_00013",
        "name": "Shapaja",
        "origin": "PISCO & ERA-5",
        "latitude": -6.827225,
        "longitude": -76.35664444,
        "ranges": []
    },
    {
        "id": "64385742843fb30d41311d76",
        "ext_id": "pe_00029",
        "name": "Saposoa",
        "origin": "PISCO & ERA-5",
        "latitude": -6.853361111,
        "longitude": -76.96205556,
        "ranges": []
    }
]
'''