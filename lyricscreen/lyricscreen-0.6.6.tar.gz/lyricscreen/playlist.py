"""

Daniel "lytedev" Flanagan
http://dmf.me

The song class containing all Song data and the logic for parsing a song from a text file.

"""

import sys
from os import path

from .song import Song
from .map import Map
from .settings import settings

class Playlist(object):
    default_dir = path.join(settings.data_dir, settings.playlists_dir)

    default_playlist_file = """Default Playlist

Default Song
"""

    def __init__(self, name = "Default"):
        self.name = name
        self.songsToLoad = []
        self.songs = []
        self.currentSong = -1
        self.file = ""

        # Display modifiers
        self.isFrozen = False
        self.isBlank = False

    def addSong(s):
        if isinstance(s, Song):
            self.songs.append(s)
        else:
            pass # possibly load song.fromFile(s)

    @staticmethod
    def load(f = "Default"):
        f = f.replace("//", "")
        f = f.replace("..", "")
        f = f.lstrip("/")
        if f.endswith(".txt"):
            f = f[:-4]
        p = Playlist("Loaded Playlist")
        raw_path = path.abspath(Playlist.default_dir + "/" + f + ".txt")
        if path.exists(raw_path):
            p.file = f
        elif f == "Default":
            fh = open(path.abspath(raw_path), 'w')
            fh.write(Playlist.default_playlist_file)
            p.file = f
        else:
            print("Warning: Playlist file doesn't exist {0}".format(path.abspath(raw_path)))
            return False
        return p.reload()

    def reload(self):
        filePath = Playlist.default_dir + "/" + self.file + ".txt"
        if not path.exists(path.abspath(filePath)):
            print("Warning: Playlist file doesn't exist {0}".format(path.abspath(filePath)))
            return False
        f = open(path.abspath(filePath))
        if not f:
            print("Error: Failed to open Playlist file {0}".format(self.file))
            return False
        self.loadSongs(self.loadHeader(f))
        return self

    def loadHeader(self, f):
        self.name = ""
        for line in f:
            l = line.strip()
            if self.name == "" and l == "":
                pass
            elif self.name != "" and l == "":
                break
            elif l[0] == "#" or (len(l) > 1 and l[0:2] == "//"):
                pass
            elif l != "" and self.name == "":
                self.name = l
        return f

    def loadSongs(self, f):
        self.songs = []
        for line in f:
            l = line.strip()
            if l == "":
                pass
            elif l[0] == "#" or l[0:2] == "//":
                pass
            elif l != "":
                self.songsToLoad.append(l)
                ls = l.split(':')
                s = Song.load(ls[0])
                if s != False:
                    if len(ls) > 1:
                        s.goToMapByName(ls[1])
                    self.songs.append(s)
                else:
                    print("Error: Failed to open Song {0}".format(l))

    def getCurrentSong(self):
        numSongs = len(self.songs)
        if numSongs == 0: return False
        self.currentSong = max(0, min(self.currentSong, numSongs - 1))
        return self.songs[self.currentSong]

    def getCurrentVerse(self):
        s = self.getCurrentSong()
        if not s: return False
        return s.getCurrentVerse()

    def goToSong(self, song_id):
        numSongs = len(self.songs)
        if numSongs == 0: return False
        self.currentSong = max(0, min(song_id, numSongs - 1))
        return self.getCurrentSong()

    def nextSong(self):
        self.currentSong += 1
        return self.getCurrentSong()

    def previousSong(self):
        """Misleadingly works like most media players in that we won't
        actually jump to the previous song unless we're on the first verse
        (title), so more accurately a "restartSong" most of the time,
        perhaps."""
        song = self.getCurrentSong()
        if song == False:
            return False
        if song.isAtStart():
            self.currentSong -= 1
            return self.getCurrentSong()
        song.goToVerse(0)
        return song

    def isAtStart(self):
        return self.currentSong == 0

    def isAtEnd(self):
        return self.currentSong == (len(self.songs) - 1)

    def goToVerse(self, verse_id):
        s = self.getCurrentSong()
        return self.getCurrentSong().goToVerse(verse_id)

    def nextVerse(self):
        s = self.getCurrentSong()
        if s.isAtEnd():
            if not self.isAtEnd():
                s = self.nextSong()
                s.restart()
                return self.getCurrentVerse()
            else:
                return False
        return self.getCurrentSong().nextVerse()

    def previousVerse(self):
        s = self.getCurrentSong()
        if s.isAtStart():
            if not self.isAtStart():
                s = self.previousSong()
                s.finish()
                return self.getCurrentVerse()
            else:
                return False
        return self.getCurrentSong().previousVerse()

    def isAtSongStart(self):
        return self.currentSong == 0

    def isAtSongEnd(self):
        return self.currentSong == (len(self.songs) - 1)

    def restart(self):
        self.currentSong = 0;
        s = self.getCurrentSong()
        if s:
            s.restart();
        return s

    def finish(self):
        self.currentSong = len(self.songs);
        s = self.getCurrentSong()
        if s:
            s.finish();
        return s

    def __str__(self):
        return '<Playlist Object {Name: '+self.name+'}>'

