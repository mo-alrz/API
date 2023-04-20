from bs4 import BeautifulSoup
import requests
import sqlite3
import re


def user_input_to_list(string, nums_list):
    """
    takes a string from the user and change it to a list of 5 integers
    """
    for st in string.split("-"):
        if st.startswith("0"):
            st = st[1:]
        nums_list.append(int(st))
    nums_list.sort()
    return nums_list


def urls_and_list_of_numbers(user_year, url_dict):
    """
    It takes user's year and makes the url of that year, after scraping all the url of dates that are in that page and
    their relevant list of winning numbers it creates and returns a dictionary of urls and their numbers
    """
    url = f'https://www.euro-jackpot.net/results-archive-{user_year}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.findAll("a")

    table_links = []
    for link in links:
        if link.find_parent('td'):
            table_links.append(f'https://www.euro-jackpot.net{link.get("href")}')

    numbers = soup.find_all("li", {"class": "ball"})
    all_numbers = []
    grouped_all_numbers = []
    for number in numbers:
        all_numbers.append(int(number.text))

    for c, i in enumerate(all_numbers, 1):
        if c % 5 == 0:
            grouped_all_numbers.append(all_numbers[c - 5:c])

    tup = list(zip(table_links, grouped_all_numbers))

    for links, numbers in tup:
        url_dict[links] = numbers

    return url_dict


def urls_and_intersections_dict(user_input, our_dict_of_data, ints_dict):
    """
    Check if user's input had any mutual numbers with lists of all winning numbers that we made in the previous
    function and if there are more than two numbers put in a dictionary and urls will be keys and number of mutual
    numbers are values
    """
    for key, value in our_dict_of_data.items():
        if len(set(value).intersection(set(user_input))) > 2:
            ints_dict[key] = len(set(value).intersection(set(user_input)))
    return ints_dict


def create_database():
    """Creating a database to store the data in it"""
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE Prizes(possibility TEXT, prize INTEGER)")
    con.commit()
    cursor.close()
    con.close()


def winning_prizes(country, ints_dict, final_result):
    """
    It checks two tables in the url, first one is default one (Hungary) and second is the region that user has selected
    then check the number of mutual numbers with Match 5, Match 4 and Match 3 and put the ones that match with each
    other in a dictionary and then add to database, we have to delete unwanted characters from the prizes so that we can
    easily treat them as integers
    """
    for url in ints_dict.keys():
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        if country == 'Hungary':
            table = soup.find('table', {'class': 'table-alt'}).find_all('td')
        else:
            table = soup.find('div', {'class': 'euro-breakdown'}).find('div', {'class': f'{country}'}) \
                .find('table', {'class': 'prize-breakdown'}).find_all('td')

        for c, i in enumerate(table):
            if i.text.strip() == 'Match 5' or i.text.strip() == 'Match 4' or i.text.strip() == 'Match 3':
                if int(i.text.strip()[-1]) == ints_dict[url]:
                    final_result[f'{url[-10:]} - {ints_dict[url]} mutual numbers'] = int(
                        ''.join(re.findall(r"\d+", table[c + 1].text[:-3])))

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    for key, value in final_result.items():
        cur.execute("INSERT INTO Prizes (possibility, prize) VALUES (?, ?)", (key, value))

    conn.commit()
    conn.close()


def sum_of_prizes():
    """ Add a row at the end of the database that shows the total prizes"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sum_prizes = cursor.execute('SELECT SUM(prize) FROM Prizes').fetchone()[0]
    cursor.execute('INSERT INTO Prizes (possibility, prize) VALUES (?, ?)', ('Total prizes', sum_prizes))
    conn.commit()
    conn.close()


def reading_data():
    """ Reads the database """
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Prizes")
    result = cursor.fetchall()
    con.close()
    return result


def clear_database():
    """ clears the database """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Prizes')
    conn.commit()
    conn.close()
