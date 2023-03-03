import requests

people = []


def all_people(api_path):
    response = requests.get(api_path)
    jsonified = response.json()
    for i in jsonified['results']:
        people.append(i['name'].lower())


def find_char(user_input):
    response = requests.get(f'https://swapi.dev/api/people/?search={user_input}')
    jsonified = response.json()

    data = ["name", "height", "mass", "hair_color", "skin_color", "eye_color"]

    for c, i in enumerate(jsonified['results'], 1):
        print(f'{c}---------------------')
        for j in data:
            print(f'{j.replace("_", " ").capitalize()} : {i[j]}')


if __name__ == "__main__":

    char = str(input('Please enter the name of character : ').lower())

    all_people('https://swapi.dev/api/people/')

    counter = len(people)
    for i in people:
        if char in i:
            find_char(char)
            break
        if char not in i:
            counter -= 1

    if counter == 0:
        print('The entered character is not in the list')
