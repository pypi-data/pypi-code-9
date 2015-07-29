#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
lib.py
Essential functions/vars to Twitch.py go here
"""

from subprocess import call
from string import printable as printable_chrs

try:
    from requests import get as re_get
except ImportError as e:
    print('Error: {0}'.format(e))
    print('Requests not installed, to install it you can run:')
    print('\n  pip install requests')
    print('Defaulting to urllib...')
    from urllib import urlopen
    from json import loads as json_load
    re_get = None
try:
    from livestreamer import streams as StreamData
    from livestreamer import __version__ as LSV
    from os.path import isfile as file_exists 
except Exception as e:
    print('Error: {0}'.format(e))
    print('Livestreamer not installed, to install it you can run:')
    print('\n  pip install livestreamer\n')
    StreamData = None
    from webbrowser import open as browser_open

class TwitchApp(object):

    API_url = 'https://api.twitch.tv/kraken'
    top_games = '{0}/games/top{1}'.format(API_url, '?limit={0}')
    search_streams = '{0}/search/streams{1}'.format(API_url, '?q={0}&limit={1}')
    default_limit = 20
    chrs = 50
    debug = False
    best = False
    livestreamer_installed = False
    requests_installed = False
    livestreamer_path = '/usr/bin/livestreamer'
    possible_paths = ['/usr/bin/livestreamer','/usr/local/bin/livestreamer']

    def __init__(self, arg_obj):
        self._import_pkgs()
        self.default_limit = arg_obj.limit
        self.best = arg_obj.best
        self.debug = arg_obj.debug

        if arg_obj.g is not None:
            return self.game_directory(' '.join(arg_obj.g))
        self.main_directory()

    def _import_pkgs(self):
        if re_get is not None:
            self.requests_installed = True
        if StreamData is not None:
            self.livestreamer_installed = True
            for path in self.possible_paths:
                if file_exists(path):
                    self.livestreamer_path = path

    def _clean_string(self, s):
        return '{0}{1}'.format(
            ''.join((x for x in s if x in printable_chrs)).strip()[:self.chrs],
            '..' if len(s) > self.chrs else '')

    def make_url(self, g, l=default_limit):
        return self.search_streams.format("%22{0}%22".format(g), l) 
    
    def get_url(self, url):
        if self.requests_installed:
            return re_get(url).json()
        return json_load(urlopen(url).read().decode('utf-8'))

    def get_input(self, disp_str, err_str, maxv):
        inp = None
        while inp is None:
            try:
                inp = int(input(disp_str))
                if inp < 1 or inp > maxv:
                    inp = None
            except ValueError:
                print(err_str)
        return inp - 1 

    def load_stream(self, url):
        print('Loading {0} ...\n'.format(url))
        if not self.livestreamer_installed:
            return browser_open(url)
        qualities = StreamData(url)
        names = [q.lower().strip() for q in qualities.keys()]
        if self.best:
            q = 'source' 
        else:
            for i, q in enumerate(names):
                print('[{ind}] {qual}'.format(ind=i+1, qual=q))
            inp = self.get_input('Enter quality> ', 'Try again', len(names))
            q = names[inp]
        print('Using quality "{0}" ...\n'.format(q))
        call([self.livestreamer_path, url, q])
        return True

    def main_directory(self):
        print('Fetching main Twitch.tv directory...')
        print('Press CTRL+C to quit\n')
        url = self.top_games.format(self.default_limit)
        if self.debug:
            print(url)
        blob = self.get_url(url)
        game_titles = [g['game']['name'] for g in blob['top']]

        for i, gt in enumerate(game_titles):
            print("{n:>2}) {0}".format(gt, n=i+1))

        inp = self.get_input('Enter number> ', 'Try again', len(game_titles))
        return self.game_directory(game_titles[inp])

    def game_directory(self, game):
        print('Getting streams for "{g}"'.format(g=game))
        print('Press CTRL+C to quit\n')
        search_key = game.lower().replace(' ', '%20')
        url = self.make_url(search_key)
        if self.debug:
            print(url)
        blob = self.get_url(url)

        streams = [(u['channel']['url'], u['channel']['status'], u['viewers'])
                    for u in blob['streams']
                    if all([x in u['channel'] for x in ('url', 'status')])]
        urls = [x[0] for x in streams]

        for i, u in enumerate(streams):
            print("{n:>2}) {status} ({name}, {views:,})".format(
                name=u[0].split("/").pop(),
                status=self._clean_string(u[1]),
                views=u[2],
                n=i+1))

        inp = self.get_input('Select stream> ', 'Try again', len(urls))
        return self.load_stream(urls[inp])

# end
