import os


def _read_file(f):
    try:
        with open(f) as h:
            return h.read()
    except:
        return None


app_dir = os.path.dirname(__file__)
version = _read_file(os.path.join(app_dir, 'version')) or '?'
app_name = 'photonemitter'
