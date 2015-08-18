"""

Daniel "lytedev" Flanagan
http://dmf.me

The song class containing all Song data and the logic for parsing a song from a text file.

"""

import sys
from os import path

from .map import Map
from .verse import Verse
from .settings import settings

class Song(object):
    default_dir = path.join(settings.data_dir, settings.songs_dir)

    default_song_file = """Default Song

Default Verse
"""

    def __init__(self, title = "Default Song"):
        self.file = ""
        self.title = title
        self.verses = []
        self.maps = []
        self.currentVerse = -1
        self.currentMap = -1

    @staticmethod
    def load(f = "Default Song"):
        s = Song()
        raw_path = Song.default_dir+"/"+f+".txt"
        if path.exists(raw_path):
            s.file = path.abspath(raw_path)
        elif f == "Default Song":
            fh = open(path.abspath(raw_path), 'w')
            fh.write(Song.default_song_file)
            s.file = path.abspath(raw_path)
        else:
            print("Warning: Song file doesn't exist {0}".format(path.abspath(raw_path)))
            return False
        return s.reload()

    def reload(self):
        if not path.exists(self.file):
            return False

        self.verses = []
        f = open(self.file, encoding="utf-8")
        if not f:
            print("Warning: Failed to open Song file {0}".format(self.file))
            return False
        self.loadVerses(self.loadHeader(f))
        self.verses.insert(0, Verse("Title", self.title))
        self.addVerse("Empty Slide")

        return self

    def addVerse(self, title, content = ""):
        if isinstance(title, Verse):
            title.name = title.name.strip()
            title.content = title.content.strip()
            self.verses.append(title)
        else:
            title = title.strip()
            self.verses.append(Verse(title, content.strip()))

    def loadHeader(self, f):
        self.title = ""
        for line in f:
            l = line.strip()
            if self.title == "" and l == "":
                pass
            elif self.title != "" and l == "":
                break
            elif l.startswith("#") or l.startswith("//"):
                pass
            elif l != "" and self.title == "":
                self.title = l
            elif self.title != "" and ":" in l:
                m = Map.fromLine(l)
                if m.verses[0] != "Title":
                    m.verses.insert(0, "Title")
                if m.verses[len(m.verses) - 1] != "Empty Verse":
                    m.verses.append("Empty Verse")
                self.maps.append(m)
        return f

    def loadVerses(self, f):
        vh = []
        v = Verse()
        gvn = 1
        for line in f:
            l = line.strip()
            if l == "":
                if v.name.strip() != "":
                    self.addVerse(v)
                    vh.append(v.name)
                    v = Verse()
            elif l[0] == "#" or l[0:2] == "//":
                pass
            elif l[0] == "(":
                l = l.strip("()")
                vh.append(l)
                pass
            elif ":" in l and v.name == "":
                v.name = line.partition(':')[0]
                v.content = ""
            elif v.name == "" and l != "":
                v.name = "Generated Verse "+str(gvn)
                v.content = l + "\n"
                gvn += 1
            elif l != "" and v.name != "":
                v.content += l + "\n"

        if v.name.strip() != "":
            v.content = v.content.strip()
            self.addVerse(v)
            vh.append(v.name)

        self.verses.append(Verse("Title", self.title))
        self.verses.append(Verse("Empty Verse", ""))

        defaultMap = Map("Default")
        vh.insert(0, "Title")
        vh.append("Empty Verse")
        defaultMap.verses = vh
        self.maps.append(defaultMap)

    def getCurrentMap(self):
        numMaps = len(self.maps)
        if numMaps == 0: return False
        self.currentMap = max(0, min(self.currentMap, numMaps - 1))
        return self.maps[self.currentMap]

    def getVerseByName(self, name):
        for v in self.verses:
            if v.name == name:
                return v
        return False

    def getCurrentVerse(self):
        map = self.getCurrentMap()
        if map == False: return False
        currentVerse = map.getCurrentVerseName()
        return self.getVerseByName(currentVerse)

    def goToVerse(self, verse_id):
        return self.getVerseByName(self.getCurrentMap().goToVerse(verse_id))

    def goToMapByName(self, name):
        i = 0
        for m in self.maps:
            if m.name == name:
                self.currentMap = i
                break
            i += 1
        return self.getCurrentMap()

    def getMapByName(self, name):
        for m in self.maps:
            if m.name == name:
                return m
        return False

    def goToMap(self, map_id):
        numMaps = len(self.maps)
        if numMaps == 0: return False
        self.currentMap = max(0, min(map_id, numMaps - 1))
        return self.getCurrentMap()

    def nextVerse(self):
        return self.getVerseByName(self.getCurrentMap().nextVerse())

    def previousVerse(self):
        return self.getVerseByName(self.getCurrentMap().previousVerse())

    def isAtStart(self):
        return self.getCurrentMap().isAtStart()

    def isAtEnd(self):
        return self.getCurrentMap().isAtEnd()

    def restart(self):
        return self.getVerseByName(self.getCurrentMap().restart())

    def finish(self):
        return self.getVerseByName(self.getCurrentMap().finish())

    def __str__(self):
        return '<Song Object {Title: '+self.title+'}>'

