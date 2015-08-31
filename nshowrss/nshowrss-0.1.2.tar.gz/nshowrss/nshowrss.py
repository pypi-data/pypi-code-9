#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    NShowRSS
"""

import logging
logging.disable(logging.CRITICAL)
from npyscreen import NPSApp, Form, TitleSelectOne
from pychapter.pychapter import Chapter
from collections import defaultdict
from imdbpie import Imdb
import fileinput
import feedparser
import argparse
import requests
import tvdb_api


class NMagnet(NPSApp):
    """
        NshowRSS - An interface to ShowRSS.info
    """

    @property
    def series_three(self):
        """
            Ordered three of series
        """
        rec = lambda: defaultdict(rec)
        base = rec()
        for chapter in self.series:
            base[chapter.series][chapter.episodeNumber] = chapter
        return base

    @property
    def series(self):
        raise NotImplementedError()

    def main(self):
        """
            Main method (ncurses stuff)
        """
        series = self.series_three

        form = Form(name='Select TV Serie')
        sel = form.add(TitleSelectOne, name="Series", values=series.keys())
        form.edit()
        serie = sel.get_selected_objects()[0]
        chapters = series[serie]

        form = Form(name='NshowRSS - Download your RSS')
        sel = form.add(TitleSelectOne, name="Chapter",
                       values=chapters.values())
        form.edit()
        self.torrent = sel.get_selected_objects()[0]


class NImdb(NMagnet):

    @property
    def series(self):
        def cache_chapter(chapter, series):
            chap = Chapter(episode=chapter["episodenumber"],
                           season=chapter["seasonnumber"],
                           series=series.title)
            chap.__repr__
            return chap

        def get_episodes(series):
            for season in t[series.title].values():
                for episode in season.values():
                    yield episode, series

        result = []
        t = tvdb_api.Tvdb()
        imdb = Imdb(cache=True)
        for show in imdb.popular_shows():
            imdbshow = imdb.get_title_by_id(show["tconst"])
            for episode, series in get_episodes(imdbshow):
                result.append(cache_chapter(episode, series))

        return result


class NShowRSS(NMagnet):
    @property
    def series(self):
        """
            Return a list of series got from the feed
        """
        def cache_chapter(ent):
            """
                Forces pychapter to get guessit info.
                For some reason, guessit produces garbage here
                (debug info).
                I guessing the ncurses library is forcing logging
                output to debug =/
            """
            c = Chapter(magnet=ent['links'][0]['href'])
            c.__repr__
            return c

        if not self.showrss_url:
            raise Exception("You need to specify a rss url")
        feed = feedparser.parse(requests.get(self.showrss_url).text).entries
        return [cache_chapter(ent) for ent in feed]


class NMagnetList(NMagnet):
    @property
    def series(self):
        """
            Gets the list of files from stdin..
            One magnet at a line
        """
        def cache_chapter(ent):
            """
                Forces pychapter to get guessit info.
                For some reason, guessit produces garbage here
                (debug info).
                I guessing the ncurses library is forcing logging
                output to debug =/
            """
            c = Chapter(magnet=ent['links'][0]['href'])
            c.__repr__
            return c
        return [cache_chapter(ent) for ent in fileinput.input()]


def main():
    """
        Main
    """
    interfaces = {
        'imdb': NImdb,
        'showrss': NShowRSS,
        'magnet': NMagnetList
    }

    parser = argparse.ArgumentParser(description='NShowRSS')
    parser.add_argument('interface', type=str,
                        help='Interface',
                        choices=['imdb', 'showrss', 'magnet'])

    parser.add_argument('--showrss_url', help="Showrss rss url",
                        nargs="?", type=str)

    args = parser.parse_args()
    main_ = interfaces[args.interface]()
    main_.showrss_url = args.showrss_url
    main_.run()
    main_.torrent.play()


if __name__ == "__main__":
    main()
