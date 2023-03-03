import requests

name = str(input('Please enter the name of character : '))
response = requests.get(f'https://swapi.dev/api/people/?search={name}')
jsonified = response.json()

data = ["name", "height", "mass", "hair_color", "skin_color", "eye_color"]

for i in jsonified['results']:
    for k,v in i.items():
        if 'Skywalker' in v:
            for x,z in i.items():
                if x in data:
                    print(f'{x} : {i[x]}')
            print(f'-------------------')
