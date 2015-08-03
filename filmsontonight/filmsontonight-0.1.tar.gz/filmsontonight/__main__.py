import sys
import time

import imdb
import viewfilm
import csv_handler

if sys.argv[1] == 'list':
    if sys.argv[2]:
        date = 'date/' + sys.argv[2]
        titles = viewfilm.get_titles(date)
    else:
        titles = viewfilm.get_titles()
    for index, title in enumerate(titles):
        print '[{0}]'.format(index) + title
    print 'Use "filmsontonight select x" to generate IMDB link'
    csv_handler.save(titles)

elif sys.argv[1] == 'select':
    try:
        index = int(sys.argv[2])
        print imdb.get_link(index)
    except TypeError:
        print 'Error: filmsontonight select requires an integer selection'
