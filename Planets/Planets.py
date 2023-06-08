from flask import Flask, render_template, jsonify, request
import requests
import re

how_many_times = {}
app = Flask(__name__)


@app.route('/planets/<name>')
def planets(name):
    pattern = r'[^a-zA-Z0-9]'
    formatted_name = re.sub(pattern, '', name).lower()

    if formatted_name not in how_many_times:
        how_many_times[formatted_name] = 0
    how_many_times[formatted_name] += 1

    response = requests.get('https://api.le-systeme-solaire.net/rest/bodies/')
    if response.status_code == 200:
        all_bodies = response.json()
        all_the_names = []
        dict_of_data = {}
        for key, value in all_bodies.items():
            for i in value:
                all_the_names.append(re.sub(pattern, '', i['englishName']).lower())
                if re.sub(pattern, '', i['englishName']).lower() == formatted_name:
                    dict_of_data['Mass'] = i["mass"]
                    dict_of_data['Volume'] = i["vol"]
                    dict_of_data['Moons'] = i["moons"]

        if formatted_name not in all_the_names:

            return 'ERROR 404 , bad request , the name is not in the list'
        return jsonify(dict_of_data)

    return '404 , page not found'


@app.route('/usage')
def usage():
    return {k: f'looked up {v} times' for (k, v) in how_many_times.items()}


if __name__ == '__main__':
    app.run(debug=True)
