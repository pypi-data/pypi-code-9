# coding: utf-8

import grab
import os
import TennisSpider.getting_time
from TennisSpider.getting_time import get_time, make_date
import csv
import sys
import argparse
from grab.spider import Spider, Task

class RanksSpider(Spider):
    initial_urls = ['http://live-tennis.eu/']
    def task_initial(self, grab, task):
        '''
        '''
        self.base_url = self.initial_urls[0]
        if self.args.c == 'm':
            if self.args.t == 'l':
                yield Task('get_ranks', url='http://live-tennis.eu/')
            elif self.args.t == 'o':
                yield Task('get_ranks', url='http://live-tennis.eu/official_atp_ranking')
            else:
                sys.stderr.write('Unvalid input of utility -t\n')
        elif self.args.c == 'f':
            if self.args.t == 'l':
                yield Task('get_ranks', url='http://live-tennis.eu/wta-live-ranking')
            elif self.args.t == 'o':
                yield Task('get_ranks', url='http://live-tennis.eu/official-wta-ranking')
            else:
                sys.stderr.write('Unvalid input of utility -t\n')
        else:
            sys.stderr.write('Unvalid input of option -c\n')

    def task_get_ranks(self, grab, task):
        '''
        Get info about ranks.
        '''
        NUM_OF_STRINGS = 5500
        NUM_OF_COLUMN = 11

        t = get_time()
        date = make_date(t[0], t[1], t[2])

        filename = os.getenv('TENNIS_FILENAME')
        xpath = '//tr/td'
        row = []
        flag = False
        with open('%s' %filename, 'a') as res:
            writer = csv.writer(res)
            for elem in grab.doc.select(xpath):
                if not flag:
                    if elem.text() == '1':
                        j = 1
                        row.append(elem.text())
                        flag = True
                else:
                    if j < NUM_OF_STRINGS:
                        if j % NUM_OF_COLUMN == (NUM_OF_COLUMN-1):
                            row.append(elem.text())
                            row.append(date)
                            writer.writerow(row)
                            row = []
                            j += 1

                        else:
                            row.append(elem.text())
                            j += 1
                    else:
                        break
