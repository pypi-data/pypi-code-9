#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    NShowRSS
"""

from npyscreen import NPSApp, Form, TitleSelectOne, TitleMultiSelect
from guessit import guess_video_info
from SimpleTorrentStreaming.SimpleTorrentStreaming import TorrentStreamer
import feedparser
import requests
import logging
import sys
import os

TCFG = os.path.expanduser('~/.nshorss.cfg')

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)


class RSSFeeder(object):
    """
        XML feeder
    """
    def __init__(self, feed_url=False):
        """
            XML Feeder.
        """

        def get_entry_data(entry):
            """
                Get title and href
            """
            return [entry['title'], entry['links'][0]['href']]

        feed = feedparser.parse(requests.get(feed_url).text).entries
        self.feed = dict([get_entry_data(entry) for entry in feed])

    def download_chapter(self, chapter):
        """
            Download chapter by title
        """
        return TorrentStreamer(TCFG).play_torrent([self.feed[chapter]])

    @property
    def chapters(self):
        """
            Get a list of chapters.
        """
        return self.feed.keys()

    def _list_chapters_info(self):
        """
            Get chapters info
        """
        return dict([[key, guess_video_info(key)] for key in self.chapters])

    @property
    def chapters_info(self):
        """
            List chapters with info ordered by tv serie
        """
        info = self._list_chapters_info().items()
        final = dict([[chapter['series'], []] for _, chapter in info])
        for full, chapter in info:
            chapter.update({'full': full, 'magnet': self.feed[full]})
            final[chapter['series']].append(Chapter().from_dict(chapter))

        return final


class Chapter(object):
    """
        Chapter object
    """
    def __init__(self):
        self.episodenumber = "NA"
        self.season = "NA"
        self.title = "NA"

    def from_dict(self, dict_):
        """
            Creates a chapter object from a given dict.
        """
        for key, value in dict_.iteritems():
            setattr(self, key.lower(), value)
        return self

    def play(self):
        """
            Uses TorrentStreamer to play the chapter
        """
        return TorrentStreamer().get_parallel_magnets(
            [self.magnet], -1, 5, "mplayer")

    def __repr__(self):
        return "Chapter {}x{} - {}".format(
            self.season,
            self.episodenumber,
            self.title
        )


class NShowRSS(NPSApp):
    """
    Curses interface
    """
    def main(self):
        global __SELECTED_TORRENTS__
        series = FEED.chapters_info

        form = Form(name='Select TV Serie')
        sel = form.add(TitleSelectOne, name="Series", values=series.keys())
        form.edit()
        serie = sel.get_selected_objects()[0]
        chapters = series[serie]

        form = Form(name='NshowRSS - Download your RSS')
        sel = form.add(TitleMultiSelect, name="Chapter", values=chapters)
        form.edit()

        __SELECTED_TORRENTS__ = sel.get_selected_objects()


def main():
    """
        Main
    """
    main_ = NShowRSS()
    main_.run()

    for torrent in __SELECTED_TORRENTS__:
        torrent.play()

FEED = RSSFeeder(sys.argv[1])
__SELECTED_TORRENTS__ = []

if __name__ == "__main__":
    main()
