# -*- coding: utf-8 -*-
"""Saves and retrieves viewfilm list of films using CSV file.

save(list) -- writes collected list to films.csv separated by '|'
get_title(index) -- retrieves title from films.csv by index
"""

import csv


def save(list):
    """Write titles to csv file.

    Pipes are /very/ uncommon in film titles so are used as the delimiter.

    Keyword arguments:
    list -- result from 'filmsontonight list'
    """
    with open('films.csv', 'wb',) as csvfile:
        filmswriter = csv.writer(csvfile, delimiter='|')
        filmswriter.writerows([list])

def get_title(index):
    """Retrieve title by index from the films.csv file, handling IOErrors.

    Keyword arguments:
    index -- int expected, from imdb.py
    """
    try:
        with open('films.csv', 'rb') as csvfile:
            filmsreader = list(csv.reader(csvfile, delimiter='|'))
            try:
                title = filmsreader[0][index]
                return title
            except IndexError:
                return 'Error: That selection was out of range'
    except IOError:
        return 'Error: Generate a list first using "filmsontonight list"'
