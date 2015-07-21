# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
import logging
import os
import re
import zlib

from babelfish import Language, language_converters
from guessit import guess_episode_info, guess_movie_info
from six.moves.xmlrpc_client import ServerProxy

from . import Provider, TimeoutSafeTransport, get_version
from .. import __version__
from ..exceptions import AuthenticationError, DownloadLimitExceeded, ProviderError
from ..subtitle import Subtitle, fix_line_ending, guess_matches
from ..video import Episode, Movie

logger = logging.getLogger(__name__)


class OpenSubtitlesSubtitle(Subtitle):
    provider_name = 'opensubtitles'
    series_re = re.compile('^"(?P<series_name>.*)" (?P<series_title>.*)$')

    def __init__(self, language, hearing_impaired, page_link, subtitle_id, matched_by, movie_kind, hash, movie_name,
                 movie_release_name, movie_year, movie_imdb_id, series_season, series_episode):
        super(OpenSubtitlesSubtitle, self).__init__(language, hearing_impaired, page_link)
        self.subtitle_id = subtitle_id
        self.matched_by = matched_by
        self.movie_kind = movie_kind
        self.hash = hash
        self.movie_name = movie_name
        self.movie_release_name = movie_release_name
        self.movie_year = movie_year
        self.movie_imdb_id = movie_imdb_id
        self.series_season = series_season
        self.series_episode = series_episode

    @property
    def id(self):
        return str(self.subtitle_id)

    @property
    def series_name(self):
        return self.series_re.match(self.movie_name).group('series_name')

    @property
    def series_title(self):
        return self.series_re.match(self.movie_name).group('series_title')

    def get_matches(self, video, hearing_impaired=False):
        matches = super(OpenSubtitlesSubtitle, self).get_matches(video, hearing_impaired=hearing_impaired)

        # episode
        if isinstance(video, Episode) and self.movie_kind == 'episode':
            # series
            if video.series and self.series_name.lower() == video.series.lower():
                matches.add('series')
            # season
            if video.season and self.series_season == video.season:
                matches.add('season')
            # episode
            if video.episode and self.series_episode == video.episode:
                matches.add('episode')
            # title
            if video.title and self.series_title.lower() == video.title.lower():
                matches.add('title')
            # guess
            matches |= guess_matches(video, guess_episode_info(self.movie_release_name + '.mkv'))
        # movie
        elif isinstance(video, Movie) and self.movie_kind == 'movie':
            # title
            if video.title and self.movie_name.lower() == video.title.lower():
                matches.add('title')
            # year
            if video.year and self.movie_year == video.year:
                matches.add('year')
            # guess
            matches |= guess_matches(video, guess_movie_info(self.movie_release_name + '.mkv'))
        else:
            logger.info('%r is not a valid movie_kind', self.movie_kind)
            return matches

        # hash
        if 'opensubtitles' in video.hashes and self.hash == video.hashes['opensubtitles']:
            matches.add('hash')
        # imdb_id
        if video.imdb_id and self.movie_imdb_id == video.imdb_id:
            matches.add('imdb_id')

        return matches


class OpenSubtitlesProvider(Provider):
    languages = {Language.fromopensubtitles(l) for l in language_converters['opensubtitles'].codes}

    def __init__(self):
        self.server = ServerProxy('https://api.opensubtitles.org/xml-rpc', TimeoutSafeTransport(10))
        self.token = None

    def initialize(self):
        logger.info('Logging in')
        response = checked(self.server.LogIn('', '', 'eng', 'subliminal v%s' % get_version(__version__)))
        self.token = response['token']
        logger.debug('Logged in with token %r', self.token)

    def terminate(self):
        logger.info('Logging out')
        checked(self.server.LogOut(self.token))
        self.server.close()
        logger.debug('Logged out')

    def no_operation(self):
        logger.debug('No operation')
        checked(self.server.NoOperation(self.token))

    def query(self, languages, hash=None, size=None, imdb_id=None, query=None, season=None, episode=None):
        # fill the search criteria
        criteria = []
        if hash and size:
            criteria.append({'moviehash': hash, 'moviebytesize': str(size)})
        if imdb_id:
            criteria.append({'imdbid': imdb_id})
        if query and season and episode:
            criteria.append({'query': query, 'season': season, 'episode': episode})
        elif query:
            criteria.append({'query': query})
        if not criteria:
            raise ValueError('Not enough information')

        # add the language
        for criterion in criteria:
            criterion['sublanguageid'] = ','.join(sorted(l.opensubtitles for l in languages))

        # query the server
        logger.info('Searching subtitles %r', criteria)
        response = checked(self.server.SearchSubtitles(self.token, criteria))
        subtitles = []

        # exit if no data
        if not response['data']:
            logger.info('No subtitles found')
            return subtitles

        # loop over subtitle items
        for subtitle_item in response['data']:
            # read the item
            language = Language.fromopensubtitles(subtitle_item['SubLanguageID'])
            hearing_impaired = bool(int(subtitle_item['SubHearingImpaired']))
            page_link = subtitle_item['SubtitlesLink']
            subtitle_id = int(subtitle_item['IDSubtitleFile'])
            matched_by = subtitle_item['MatchedBy']
            movie_kind = subtitle_item['MovieKind']
            hash = subtitle_item['MovieHash']
            movie_name = subtitle_item['MovieName']
            movie_release_name = subtitle_item['MovieReleaseName']
            movie_year = int(subtitle_item['MovieYear']) if subtitle_item['MovieYear'] else None
            movie_imdb_id = int(subtitle_item['IDMovieImdb'])
            series_season = int(subtitle_item['SeriesSeason']) if subtitle_item['SeriesSeason'] else None
            series_episode = int(subtitle_item['SeriesEpisode']) if subtitle_item['SeriesEpisode'] else None

            subtitle = OpenSubtitlesSubtitle(language, hearing_impaired, page_link, subtitle_id, matched_by, movie_kind,
                                             hash, movie_name, movie_release_name, movie_year, movie_imdb_id,
                                             series_season, series_episode)
            logger.debug('Found subtitle %r', subtitle)
            subtitles.append(subtitle)

        return subtitles

    def list_subtitles(self, video, languages):
        query = season = episode = None
        if isinstance(video, Episode):
            query = video.series
            season = video.season
            episode = video.episode
        elif ('opensubtitles' not in video.hashes or not video.size) and not video.imdb_id:
            query = video.name.split(os.sep)[-1]

        return self.query(languages, hash=video.hashes.get('opensubtitles'), size=video.size, imdb_id=video.imdb_id,
                          query=query, season=season, episode=episode)

    def download_subtitle(self, subtitle):
        logger.info('Downloading subtitle %r', subtitle)
        response = checked(self.server.DownloadSubtitles(self.token, [str(subtitle.subtitle_id)]))
        subtitle.content = fix_line_ending(zlib.decompress(base64.b64decode(response['data'][0]['data']), 47))


class OpenSubtitlesError(ProviderError):
    """Base class for non-generic :class:`OpenSubtitlesProvider` exceptions."""
    pass


class Unauthorized(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '401 Unauthorized'."""
    pass


class NoSession(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '406 No session'."""
    pass


class DownloadLimitReached(OpenSubtitlesError, DownloadLimitExceeded):
    """Exception raised when status is '407 Download limit reached'."""
    pass


class InvalidImdbid(OpenSubtitlesError):
    """Exception raised when status is '413 Invalid ImdbID'."""
    pass


class UnknownUserAgent(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '414 Unknown User Agent'."""
    pass


class DisabledUserAgent(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '415 Disabled user agent'."""
    pass


class ServiceUnavailable(OpenSubtitlesError):
    """Exception raised when status is '503 Service Unavailable'."""
    pass


def checked(response):
    """Check a response status before returning it.

    :param response: a response from a XMLRPC call to OpenSubtitles.
    :return: the response.
    :raise: :class:`OpenSubtitlesError`

    """
    status_code = int(response['status'][:3])
    if status_code == 401:
        raise Unauthorized
    if status_code == 406:
        raise NoSession
    if status_code == 407:
        raise DownloadLimitReached
    if status_code == 413:
        raise InvalidImdbid
    if status_code == 414:
        raise UnknownUserAgent
    if status_code == 415:
        raise DisabledUserAgent
    if status_code == 503:
        raise ServiceUnavailable
    if status_code != 200:
        raise OpenSubtitlesError(response['status'])

    return response
