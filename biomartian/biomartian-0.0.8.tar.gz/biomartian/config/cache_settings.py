from os.path import expanduser, join as path_join

from joblib import Memory

default_cache_path = path_join(expanduser("~"), ".biomartian/")
memory = Memory(cachedir=default_cache_path, verbose=0)
