class Well(object):
    def __init__(self, x, y, path, name=''):
        self.x = x
        self.y = y
        self.path = path
        self.name = name

class GocadWellReader(object):
    def __init__(self, filename):
        self.filename = filename


