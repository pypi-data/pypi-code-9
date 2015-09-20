#!/usr/bin/env python
# coding: utf-8

import grab
import os
import csv
import sys
import argparse
from grab.spider import Spider, Task

class ScheduleSpider(Spider):
    initial_urls = ['http://www.tennislive.net/', ]
    def task_initial(self, grab, task):
        '''
        '''
        date = ''
        if os.getenv('DATE') != None:
            date = os.getenv('DATE')
        self.base_url = self.initial_urls[0]
        task.url = 'http://www.tennislive.net/{}'.format(date)
        yield Task('schedule', url=task.url)

    def task_schedule(self, grab, task):
        '''
        Go to the site with schedule
        '''
        xpath = '//div[@class = "full"]/ul/li/a'
        for elem in grab.doc.select(xpath):
            if elem.text() == "Scheduled":
                new_url = elem.attr('href')
                sys.stdout.write("Schedule:")
                yield Task('get_pairs', new_url)

    def task_get_pairs(self, grab, task):
        '''
        Iterate on all mathes in schedule.
        '''
        xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
        for elem in grab.doc.select(xpath):
            if elem.attr('class') == "head2head":
                el = elem.select('a')
                stats_url = el.attr('href')
                yield Task('get_info', stats_url)

    def task_get_info(self, grab, task):
        '''
        Get info about match in schedule.
        '''
        NUM_OF_COLUMN = 6
        xpath = '//div[@class="player_matches"]/table/tr/td'
        i = 0
        match = []
        for elem in grab.doc.select(xpath):
            if i < NUM_OF_COLUMN:
                if elem.text() != '':
                    match.append(str(elem.text()))
                i += 1
            elif i == NUM_OF_COLUMN:
                if elem.text() != '':
                    match.append(str(elem.text()))
                break
        flag = False
        for elem in match:
            if elem != 'no matches found':
                sys.stdout.write(elem + ', ')
                flag = True
        if flag:
            sys.stdout.write('\n')