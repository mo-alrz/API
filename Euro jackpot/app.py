from flask import Flask, render_template, request
import functions as funcs
import os.path
import threading

app = Flask(__name__)


@app.route('/')
def index():
    """
    If there already is a database and user wants to refresh the main page and go for another round we have
    to clean it so there will be no conflict with the previous results and if this is the first round it will
    automatically build the database
    """
    if request.method == 'GET':
        if os.path.isfile('database.db'):
            funcs.clear_database()
        else:
            funcs.create_database()

    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        year = request.form['year']
        country = request.form['country']
        numbers = request.form['numbers']
        lookback = request.form['lookback']

        numbers_list = []
        funcs.user_input_to_list(numbers, numbers_list)
        # change the user's input numbers to the required format

        def multi_threading():
            """ put the main operation in a function, so it can be done in by multi threading """
            urls_and_list_of_numbers_dict = {}
            funcs.urls_and_list_of_numbers(yr, urls_and_list_of_numbers_dict)

            urls_and_intersections_dict = {}
            funcs.urls_and_intersections_dict(numbers_list, urls_and_list_of_numbers_dict, urls_and_intersections_dict)

            last_result = {}
            funcs.winning_prizes(country, urls_and_intersections_dict, last_result)

        threads = []

        for yr in range(int(year) - int(lookback) + 1, int(year) + 1):
            # Appending threads in a list , so we can loop through them and use join()
            t = threading.Thread(target=multi_threading)
            threads.append(t)
            t.start()

        for thrd in threads:
            # Looping through threads and join()
            thrd.join()

    funcs.sum_of_prizes()
    results = funcs.reading_data()
    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
