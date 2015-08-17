import zlib


class ZlibCodec(object):
    def encode(self, data):
        return zlib.compress(data)

    def decode(self, data):
        return zlib.decompress(data)
