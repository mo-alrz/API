import pyodbc
from flask import Flask, render_template, request, jsonify
# from flask_api_key import APIKeyManager

app = Flask(__name__)

jsonified = []


def database_to_json():
    connection = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/malir/desktop/"
                                r"API/REST-API-with-Python-Flask/movies.accdb")
    cursor = connection.cursor()
    cursor.execute('select * from Movies')
    keys = [i[0] for i in cursor.execute('select * from Movies').description]
    for i in cursor.fetchall():
        jsonified.append(dict(zip(keys, i)))


@app.route('/')
def index():
    return render_template('read_me.html')


@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        database_to_json()
        return jsonified

    if request.method == 'POST':
        data = request.get_json(force=True)
        director = data['director']
        name = data['name']
        genre = data['genre']
        year = data['year']

        connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/malir/'
                                    r'desktop/API/REST-API-with-Python-Flask/movies.accdb')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Movies (Name, Director, Production_year, Genre)
            VALUES (?, ?, ?, ?)
        ''', (name, director, year, genre))

        connection.commit()
        database_to_json()
        return jsonified


@app.route('/movies/<int:movie_id>')
def movies_by_id(movie_id):
    database_to_json()
    for movie in jsonified:
        if movie["ID"] == movie_id:
            return movie
        continue
    return f'{movie_id} is an invalid ID in Database'


if __name__ == '__main__':
    app.run(debug=True)
