import requests

response = requests.get('https://get.geojs.io/v1/ip/geo.json')
jsonified = response.json()
long = jsonified['longitude']
lat = jsonified['latitude']

weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true&hourly=" \
          f"temperature_2m,relativehumidity_2m,windspeed_10m"

response2 = requests.get(f'{weather}')
jsonified = response2.json()
for k,v in jsonified["current_weather"].items():
    print(f'{k} : {v}')