"""

Daniel "lytedev" Flanagan
http://dmf.me

"""

class Verse(object):
    def __init__(self, name = "", content = ""):
        self.name = name
        self.content = content

    def getExcerpt(self):
        excerpt = (self.content[:50] + '..') if len(self.content) > 50 else self.content
        return excerpt.split("\n")[0]

    def __str__(self):
        return "("+self.name+"):\n"+("\n".join(self.content.split("\n")))

