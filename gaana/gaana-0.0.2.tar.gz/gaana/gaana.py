#!/usr/bin/env python
# pylint: disable=C0325,W0603

"""Gaana!!"""

import os
import requests
import re
import argparse
from terminaltables import AsciiTable
from base64 import b64encode
from base64 import b64decode
import hmac


class BadHTTPCodeError(Exception):

    """Bad http code error"""

    def __init__(self, code):
        super(BadHTTPCodeError, self).__init__()
        print(code)


class GaanaDownloader(object):

    """Gaana downloader class."""

    def __init__(self):
        base_url = 'http://api.gaana.com'
        index_url = '%s/index.php' % base_url
        self.urls = {
            'search': 'http://gaana.com/search/songs/{query}',
            'get_token': 'http://gaana.com//streamprovider/get_stream_data_v1.php',
            'search_album': 'http://gaana.com/search/albums/{query}',
            'search_artist': 'http://gaana.com/search/artists/{query}',
            'album': 'http://gaana.com/album/{name}',
            'artist': 'http://gaana.com/artist/{name}',
            'search_songs_new': (
                '%s?type=search&subtype=search_song&content_filter=2&key={query}' % index_url),
            'search_albums_new': (
                '%s?type=search&subtype=search_album&content_filter=2&key={query}' % index_url),
            'get_song_url': (
                '%s/getURLV1.php?quality=high&album_id={album_id}'
                '&delivery_type=stream&hashcode={hashcode}&isrc=0&type=rtmp'
                '&track_id={track_id}' % base_url),
            'album_details': (
                '%s?type=album&subtype=album_detail&album_id={album_id}' % index_url),
            'playlist_details': (
                '%s?type=playlist&subtype=playlist_detail&playlist_id={playlist_id}' % index_url),
            'get_playlists': (
                '%s?type=playlist&subtype=topCharts&limit=0,15&orderby=popularity' % index_url)
        }

    @classmethod
    def _get_url_contents(cls, url):
        """Return url response if successful or 200"""
        url = url.replace(' ', '%20')
        response = requests.get(url)
        if response.status_code == 200:
            return response
        raise BadHTTPCodeError(response.status_code)

    @classmethod
    def _create_hashcode(cls, track_id):
        """Create and return hascode wrap with key."""
        key = 'ec9b7c7122ffeed819dc1831af42ea8f'
        hashcode = hmac.new(key, b64encode(track_id)).hexdigest()
        return hashcode

    def _get_song_url(self, track_id, album_id):
        """Return song url in order to download it."""
        url = self.urls['get_song_url']
        hashcode = self._create_hashcode(track_id)
        url = url.format(
            track_id=track_id, album_id=album_id, hashcode=hashcode)
        response = requests.get(
            url, headers={'deviceType': 'GaanaAndroidApp', 'appVersion': 'V5'})
        song_url_b64 = response.json()['data']
        song_url = b64decode(song_url_b64)
        return song_url

    def _download_track(self, song_url, track_name, dir_name):
        """Download track from give url."""
        # make sure that the name does not contain following characters < > | /
        # \ : ? * "
        pattern = re.compile(r'<|>|\\|/|:|\*|\||\?|"')
        track_name = pattern.sub('_', track_name)
        if 'mp3' in song_url:
            track_name = track_name + '.mp3'
        else:
            track_name = track_name + '.mp4'
        file_path = dir_name + '/' + track_name
        print 'Downloading to', file_path
        response = self._get_url_contents(song_url)
        with open(file_path, 'wb') as file_pointer:
            file_pointer.write(response.content)

    @classmethod
    def _check_path(cls, _dir):
        """Check dir exits, if not create it."""
        if _dir and not os.path.exists(_dir):
            os.system('mkdir %s' % _dir)

    @classmethod
    def _check_input(cls, ids, len_of_tracks):
        """Validate given ids."""
        ids = [sid.strip() for sid in ids.split(',')]
        for i in ids:
            if not i.isdigit() or int(i) > len_of_tracks:
                return False
        return True

    def search_songs(self, query, _dir):
        """Search and provide option to select song."""
        if not _dir:
            _dir = 'misc'
        self._check_path(_dir)
        url = self.urls['search_songs_new']
        url = url.format(query=query)
        response = self._get_url_contents(url)
        tracks = response.json()['tracks']
        if tracks:
            tracks_list = [
                [track['track_title'], track['track_id'], track['album_id'],
                 track['album_title'],
                 ','.join([artist['name'] for artist in track['artist']]),
                 track['duration']]
                for track in tracks]
            tabledata = [['S No.', 'Track Title', 'Track Artist', 'Album']]
            for idx, value in enumerate(tracks_list):
                tabledata.append([str(idx), value[0], value[4], value[3]])
            table = AsciiTable(tabledata)
            print table.table
            idx = raw_input(
                'Which album do you wish to download? Enter S No. :')
            while not self._check_input(idx, len(tracks_list) - 1):
                print 'Oops!! You made some error in entering input'
                idx = raw_input(
                    'Which album do you wish to download? Enter S No. :')
            idx = int(idx)
            song_url = self._get_song_url(
                tracks_list[idx][1], tracks_list[idx][2])
            self._download_track(
                song_url, tracks_list[idx][0].replace(' ', '-'), _dir)
        else:
            print 'Ooopsss!!! Sorry no track found matching your query'
            print 'Why not try another Song? :)'

    def search_albums(self, query, _dir=None):
        """Search and provide option to select album."""
        url = self.urls['search_albums_new']
        url = url.format(query=query)
        response = self._get_url_contents(url)
        albums = response.json().get('album')
        if albums:
            albums_list = [
                [album['album_id'],
                 album['title'],
                 album['language'],
                 album['seokey'],
                 album['release_date'],
                 ','.join([artist['name']
                           for artist in album.get('artists', [])[:2]]),
                 album['trackcount']]
                for album in albums]
            tabledata = [['S No.', 'Album Title', 'Album Language',
                          'Release Date', 'Artists', 'Track Count']]
            for idx, value in enumerate(albums_list):
                tabledata.append(
                    [str(idx), value[1], value[2], value[4], value[5], value[6]])
            table = AsciiTable(tabledata)
            print table.table
            idx = int(
                raw_input('Which album do you wish to download? Enter S No. :'))
            album_details_url = self.urls['album_details']
            album_details_url = album_details_url.format(
                album_id=albums_list[idx][0])
            response = requests.get(
                album_details_url,
                headers={'deviceType': 'GaanaAndroidApp', 'appVersion': 'V5'}
            )
            tracks = response.json()['tracks']
            tracks_list = [
                [track['track_title'].strip(),
                 track['track_id'],
                 track['album_id'],
                 track['album_title'],
                 ','.join([artist['name'] for artist in track['artist']]),
                 track['duration']]
                for track in tracks]
            print 'List of tracks for ', albums_list[idx][1]
            tabledata = [['S No.', 'Track Title', 'Track Artist']]
            idy = None
            for idy, value in enumerate(tracks_list):
                tabledata.append([str(idy), value[0], value[4]])
            if idy is not None:
                tabledata.append(
                    [str(idy + 1), 'Enter this to download them all.', ''])
            table = AsciiTable(tabledata)
            print table.table
            print 'Downloading tracks to %s folder' % albums_list[idx][3]
            ids = raw_input('Please enter csv of S no. to download:')
            while not self._check_input(ids, len(tracks_list)) or not ids:
                print 'Oops!! You made some error in entering input'
                ids = raw_input('Please enter csv of S no. to download:')
            if not _dir:
                _dir = albums_list[idx][3]
            self._check_path(_dir)
            ids = map(int, [sid.strip() for sid in ids.split(',')])
            if len(ids) == 1 and ids[0] == idy + 1:
                for item in tracks_list:
                    song_url = self._get_song_url(item[1], item[2])
                    self._download_track(
                        song_url, item[0].replace(' ', '-').strip(), _dir)
            else:
                for i in ids:
                    item = tracks_list[i]
                    song_url = self._get_song_url(item[1], item[2])
                    self._download_track(
                        song_url, item[0].replace(' ', '-').strip(), _dir)
        else:
            print 'Ooopsss!!! Sorry no such album found.'
            print 'Why not try another Album? :)'

    def search_playlists(self):
        url = self.urls['get_playlists']
        response = self._get_url_contents(url)
        playlist = response.json()['playlist']
        if playlist:
            playlists = [
                [lst['popularity'], lst['title'], lst['language'],
                 lst['trackids'], lst['playlist_id'], lst['createdby']]
                for lst in playlist]
            tabledata = [
                ['S No.', 'Playlist Name', 'Language', 'Popularity', 'Createdby']]
            for idx, value in enumerate(playlists):
                tabledata.append(
                    [str(idx), value[1], value[2], value[0], value[5]])
            table = AsciiTable(tabledata)
            print table.table
            idx = int(
                raw_input('Which playlist do you wish to download? Enter S No. :'))
            playlist_details_url = self.urls['playlist_details']
            playlist_details_url = playlist_details_url.format(
                playlist_id=playlists[idx][4])
            # print 'Playlist : ', playlist_details_url
            response = requests.get(playlist_details_url)
            tracks = response.json()['tracks']
            # print 'tracks : ', response.json()
            tracks_list = [
                [track['track_title'].strip(),
                 track['track_id'],
                 track['album_id'],
                 track['album_title'],
                 ','.join([artist['name'] for artist in track['artist']]),
                 track['duration']]
                for track in tracks]
            # print 'List of tracks for ', playlists[idx][1]
            # print 'List of tracks for ', tracks_list
            tabledata = [['S No.', 'Track Title', 'Track Artist']]
            idy = None
            for idy, value in enumerate(tracks_list):
                tabledata.append([str(idy), value[0], value[4]])
            if idy is not None:
                tabledata.append(
                    [str(idy + 1), 'Enter this to download them all.', ''])
            table = AsciiTable(tabledata)
            print table.table
            print 'Downloading tracks to %s folder' % playlists[idx][1]
            ids = raw_input('Please enter csv of S no. to download:')
            while not self._check_input(ids, len(tracks_list)) or not ids:
                print 'Oops!! You made some error in entering input'
                ids = raw_input('Please enter csv of S no. to download:')
            _dir = playlists[idx][1].replace(' ', '-')
            print 'using dir:', _dir
            if not _dir:
                print 'changing dir'
                _dir = playlists[idx][1]
                print 'using dir:', _dir
            self._check_path(_dir)
            ids = map(int, [sid.strip() for sid in ids.split(',')])
            if len(ids) == 1 and ids[0] == idy + 1:
                for item in tracks_list:
                    song_url = self._get_song_url(item[1], item[2])
                    self._download_track(
                        song_url, item[0].replace(' ', '-').strip(), _dir)
            else:
                for i in ids:
                    item = tracks_list[i]
                    song_url = self._get_song_url(item[1], item[2])
                    self._download_track(
                        song_url, item[0].replace(' ', '-').strip(), _dir)
        else:
            print 'Ooopsss!!! Sorry no such album found.'
            print 'Why not try another Album? :)'


def _setup():
    """Setup parser if executed script directly."""
    parser = argparse.ArgumentParser(description='Download from gaana.com')
    parser.add_argument(
        '-a', '--album', nargs='?', type=str,
        help='choose this to search albums. Space seperated query must be enclosed in quotes(\'\')')
    parser.add_argument(
        '-s', '--song', nargs='?', type=str,
        help='choose this to search songs. Space seperated query must be enclosed in quotes(\'\')')
    parser.add_argument(
        '-p', '--playlists', nargs='?',
        help='can be used to load default playlists', type=str)
    parser.add_argument(
        '-d', '--dir', nargs='?',
        help='can be used to specify directory to download songs to', type=str)
    return parser.parse_args()


def main():
    """Entry point."""
    args = _setup()
    gaana_downloader = GaanaDownloader()
    if args.album:
        gaana_downloader.search_albums(args.album, args.dir)
    elif args.song:
        gaana_downloader.search_songs(args.song, args.dir)
    gaana_downloader.search_playlists()

if __name__ == '__main__':
    main()
