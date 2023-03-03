import requests

name = "han solo"
response = requests.get(f'https://swapi.dev/api/people/?search={name}')
jsonified = response.json()


data = ["name", "height", "mass", "hair_color", "skin_color", "eye_color"]

for i in data:
    print(f'{i} : {jsonified["results"][0][i]}')
