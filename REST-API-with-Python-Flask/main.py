import pyodbc
from flask import Flask

app = Flask(__name__)
mgr = APIKeyManager(app)

jsonified = []


def database_to_json():
    connection = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/malir/desktop/"
                                r"API/REST-API-with-Python-Flask/movies.accdb")
    cursor = connection.cursor()
    cursor.execute('select * from Movies')
    keys = [i[0] for i in cursor.execute('select * from Movies').description]
    for i in cursor.fetchall():
        jsonified.append(dict(zip(keys, i)))


@app.route('/movies')
def movies():
    database_to_json()
    return jsonified


@app.route('/movies/<int:movie_id>')
def movies_by_id(movie_id):
    database_to_json()
    for movie in jsonified:
        if movie["ID"] == movie_id:
            return movie


if __name__ == '__main__':
    app.run(debug=True)
