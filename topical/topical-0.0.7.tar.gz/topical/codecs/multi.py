

class MultiCodec(object):
    """
    A codec which simply composes together a chain of other codecs
    """

    def __init__(self, *codecs):
        self.codecs = codecs

    def encode(self, data):
        for codec in self.codecs:
            data = codec.encode(data)
        return data

    def decode(self, data):
        for codec in reversed(self.codecs):
            data = codec.decode(data)
        return data
