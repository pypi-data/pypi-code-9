from path import Path
from StringIO import StringIO


EMPTY_GIF_BASE64 = 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
HELLOWORLD_BASE64 = 'cHJpbnQgIkhlbGxvIFdvcmxkIgo='


def asset(filename):
    path = Path(__file__).dirname().realpath().joinpath('assets', filename)
    return path


def asset_as_StringIO(filename):
    result = StringIO(asset(filename).bytes())
    result.filename = filename
    return result
