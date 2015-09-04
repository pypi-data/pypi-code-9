# -*- coding:utf-8 -*-

import re
import redis
import datetime
import urlparse
import socket
import json

try:
    from django.conf import settings
except ImportError:
    import config as settings

from bs4 import BeautifulSoup

from .utils import get_normal_url
from .mixin import openYandexMixin

MAX_OPEN_LINKS = 50


class TimeoutError(Exception):
    pass


def getData(s):
    data = ''
    text = ''
    now = datetime.datetime.now()

    while True:
        data += s.recv(1024)
        if (datetime.datetime.now() - datetime.timedelta(seconds=60)) > now:
            raise TimeoutError

        if '###end###' in data:
            text = data.replace('###end###', '')
            break
    return BeautifulSoup(text)


def getServer(s):
    data = ''
    text = ''
    now = datetime.datetime.now()

    while True:
        data += s.recv(1024)
        if (datetime.datetime.now() - datetime.timedelta(seconds=60)) > now:
            raise TimeoutError

        if '###end###' in data:
            text = data.replace('###end###', '')
            break
    server, port = text.split(':')
    return text, server, int(port)


class openYandex(openYandexMixin):

    def __init__(self, key):
        self.key = key
        self.rds = redis.Redis(**settings.ANTI_REDIS_CONF)
        self.state = {'counter': 0, 'state': True}

    def setUp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(120)
        s.connect(settings.ANTI_BALANCER)
        string = "###GET_SERVER###"
        s.send(string)
        self.redis_key, self.server, self.port = getServer(s)
        try:
            self.state = json.loads(self.rds.get(self.redis_key))
        except (ValueError, TypeError):
            pass

    def restart_browser(self):
        string = '###restart###'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(120)
        print self.server + ':' + str(self.port)
        s.connect((self.server, self.port))
        s.send(string)
        getData(s)

    def update_state(self):
        """ Обновление состояния браузера и рестарт в случае надобности """
        if hasattr(self, 'redis_key'):
            self.state['counter'] += 1
            if self.state['counter'] >= MAX_OPEN_LINKS:
                self.restart_browser()
                self.state['counter'] = 0
            self.state['state'] = False
            self.rds.set(self.redis_key, json.dumps(self.state))

    def get_soup(self, url, save=True, counter=0, normalize=False):
        try:
            self.setUp()
            self.save = save
            self.counter = counter
            self.normalize = normalize

            self.url = url
            parse_url = urlparse.urlparse(url)
            self.hostname = parse_url.hostname
            self.query = parse_url.query

            if isinstance(self.query, unicode):
                self.query = self.query.encode('utf8')

            string = '###split###'.join((url, self.key))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(120)
            print self.server + ':' + str(self.port)
            s.connect((self.server, self.port))
            s.send(string)
            soup = getData(s)
            if save:
                data = self.saveData(soup)
                if normalize:
                    return data
            return soup

        except (TimeoutError, socket.timeout) as exc:
            print exc
            counter += 1
            if counter > 5:
                return BeautifulSoup('<p>%s</p>' % str(exc))
            return self.get_soup(url, save=save, counter=counter, normalize=normalize)

        except KeyboardInterrupt as e:
            raise e

        except Exception as e:
            raise e

        finally:
            self.update_state()

    def formatData(self, soup):
        """ Формирование данных """
        data = []
        if 'yandex.ru' == self.hostname:

            blocks = soup.find_all(class_='serp-block')
            if blocks:
                blocks = [item for item in blocks
                          if len(item.attrs.get('class')) < 3 or 'serp-block_type_site' in item.attrs.get('class')]

                params = urlparse.parse_qs(self.query)
                key = params['text'][0]

                pos = int(params['p'][0]) if 'p' in params else 0
                pos = int(params['numdoc'][0])*pos if 'numdoc' in params else pos*10
                lr = int(params['lr'][0]) if 'lr' in params else 0

                for block in blocks:
                    for item in block:
                        tlink = item.find('a', class_='serp-url__link')
                        if tlink:
                            pos += 1
                            host = get_normal_url(tlink['href'])
                            if 'yandex.ru' not in host and 'infected?' not in host:
                                url = item.find('a', class_='serp-item__title-link').get('href')
                                data.append((pos, key.decode('utf8'), host, url, 0, lr))
            if len(blocks) == 0:
                if unicode(soup).find(u'По вашему запросу ничего не нашлось') == -1:
                    self.get_soup(self.url, self.save, self.counter, self.normalize)

        if 'www.google.ru' == self.hostname:
            params = urlparse.parse_qs(self.query)
            key = params['q'][0]
            pos = int(params['start'][0]) if 'start' in params else 0

            for item in soup.findAll('li', {'class': 'g'}):
                pos += 1
                if item.find('cite'):
                    res = re.search(r'(https://)?(www.)?([^/\ ]+)', item.find('cite').text)
                    if res:
                        host = get_normal_url(res.group())
                        data.append((pos, key.decode('utf8'), host, None, 1, None))

        return data

    def saveData(self, soup):
        """ Сохранение в postgre """
        data = self.formatData(soup)
        self.rds.set('page:' + self.url, json.dumps(data))
        return data


openGoogle = openYandex
