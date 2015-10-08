from functools import wraps
import inspect

def safe_leveldb(x, dbs = {}):
    '''
    Singleton leveldb objects
    '''
    y = os.path.abspath(os.path.expanduser(x))
    if y in dbs:
        pass
    elif os.path.exists(y) and not os.path.isdir(y):
        raise TypeError('"%s" is not a directory.')
    else:
        dbs[y] = leveldb.LevelDB(y)
    return dbs[y]

class Plugin(object):
    name = 'leveldb'
    api = 2

    def __init__(self, db, keyword = 'leveldb'):
        self.db = db
        self.keyword = keyword

    def setup(self, app):
        pass

    def apply(self, callback, context):
        args = inspect.getargspec(context.callback)[0]
        if self.keyword in args:
            @wraps(callback)
            def wrapper(*args, **kwargs):
                kwargs[self.keyword] = self.db
                return callback(*args, **kwargs)
            return wrapper
        else:
            return callback

    def close(self):
        pass
