import sys


def load_module(path, filename):
    filename = filename.strip('.py')
    sys.path.insert(0, path)
    module = __import__(filename)
    del sys.path[0]
    return module
