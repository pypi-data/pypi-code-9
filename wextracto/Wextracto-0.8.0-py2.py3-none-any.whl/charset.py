class CharsetR

class Readable(object):

    def __init__(self, fp):
        self.

    def read(self, 



class CharsetReadable(object):

    def __init__(self, response):
        self.candidate_charsets = ['windows-1252']
        self.response = response
        self.charset_parser = CharsetParser()
        self.lookahead()

    def lookahead(self):
        chunks = []
        while True:
             chunk = self.response.read(1024)
             self.chunks.append(chunk)
             try:
                 self.charset_parser.feed(chunk)
             except StopFeeding:
                 pass

    def read(self, size=None):

        dirty = 
        if self.charset_parser.parsing:
             self.charset_parser.feed(





