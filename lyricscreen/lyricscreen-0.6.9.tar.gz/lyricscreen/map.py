"""

Daniel "lytedev" Flanagan
http://dmf.me

"""

class Map(object):
    def __init__(self, name = "Default"):
        self.name = name
        self.currentVerse = -1
        self.verses = []

    def __str__(self):
        return self.name+": "+(', '.join(self.verses))

    @staticmethod
    def fromLine(line):
        m = Map()
        if ":" not in line:
            return False
        d = line.partition(':')
        m.name = d[0]
        m.verses = list(i.strip() for i in d[2].strip().split(','))
        return m

    def getCurrentVerseName(self):
        numVerses = len(self.verses)
        if numVerses == 0: return False
        self.currentVerse = max(0, min(self.currentVerse, numVerses - 1))
        return self.verses[self.currentVerse]

    def goToVerse(self, verse_id):
        numVerses = len(self.verses)
        if numVerses == 0: return False
        self.currentVerse = max(0, min(verse_id, numVerses - 1))
        return self.getCurrentVerseName()

    def nextVerse(self):
        self.currentVerse += 1
        return self.getCurrentVerseName()

    def previousVerse(self):
        self.currentVerse -= 1
        return self.getCurrentVerseName()

    def isAtStart(self):
        return self.currentVerse == 0

    def isAtEnd(self):
        return self.currentVerse == (len(self.verses) - 1)

    def restart(self):
        self.currentVerse = 0
        return self.getCurrentVerseName()

    def finish(self):
        self.currentVerse = len(self.verses) - 1
        return self.getCurrentVerseName()

