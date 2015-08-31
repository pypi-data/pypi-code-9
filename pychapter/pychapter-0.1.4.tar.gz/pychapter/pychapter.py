#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Chapter management.

    Gets chapter info from a magnet link.
    Can be also used to get chapter info from a filename,
    or just get a list of ordered chapters.
"""

from guessit import guess_video_info
import urlparse
from SimpleTorrentStreaming.SimpleTorrentStreaming import TorrentStreamer


class Chapter(object):
    """
        Chapter object
        Create new chapter with:

            ::

                Chapter(
                    'title': title,
                    'magnet': magnet,
                    'season': season,
                    'episode': episodeNumber,
                    'filename': filename
                )

        if magnet is not specified, it'll look into eztv for it.
        if episodenumber and season not specified, but file
    """
    def __init__(self, title="NA", season="NA", episode="NA", series="NA",
                 filename=False,
                 magnet=False):
        self._episodeNumber = episode
        self._season = season
        self._title = title
        self._filename = filename
        self._series = series
        self._video_info
        self.magnet = magnet

    def get_cap(self, cap):
        """
            Returns a video property.
            This being:

            - title
            - season
            - series
            - episodeNumber

            If they're not set, it tries to get them from video
            info using `guessit`
        """
        cap_ = cap.replace('_', '')
        if getattr(self, cap) == "NA" or not getattr(self, cap):
            if not self.filename:
                return "NA"
            if cap_ in self.video_info.keys():
                setattr(self, cap, self.video_info[cap_])
        return getattr(self, cap)

    @property
    def filename(self):
        """
            Return filename.
            If not filename defined, it'll try to get it from the magnet link
        """
        if not self._filename:
            if not self.magnet:
                return False
            qstring = urlparse.urlparse(self.magnet).query
            self._filename = urlparse.parse_qs(qstring)['dn'][0]

        return self._filename

    @property
    def video_info(self):
        if not self._video_info:
            self._video_info = guess_video_info(self.filename)
        return self._video_info

    @property
    def episodeNumber(self):
        return self.get_cap('_episodeNumber')

    @property
    def title(self):
        return self.get_cap('_title')

    @property
    def season(self):
        return self.get_cap('_season')

    @property
    def series(self):
        return self.get_cap('_series')

    def play(self):
        """
            Uses TorrentStreamer to play the chapter
        """
        return TorrentStreamer().get_parallel_magnets(
            [self.magnet], -1, 5, "mplayer")

    def __repr__(self):
        return "Chapter {}x{} - {} ({})".format(
            self.season,
            self.episodeNumber,
            self.title,
            self.series
        )
