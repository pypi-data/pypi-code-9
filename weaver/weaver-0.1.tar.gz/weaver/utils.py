import inspect
import re
from fabric.api import env

def _(_string, flags=[], config={}):
    """
    Takes string and applies locals to string
    Args:
        flags list<string>:
            oneline
        config dict:
            enable_globals bool (false):
    """
    enable_globals = config.get('enable_globals', False)
    frame = inspect.currentframe()
    _locals = frame.f_back.f_locals
    if enable_globals:
        _locals.update(globals())
    res = _string.format(**_locals)
    for f in flags:
        res = flag_handler(f, res)
    return res

def flag_handler(flag, res):
    if (flag == "oneline"):
        res = re.sub('\n\s+', ' ', res)
    elif(flag == "print"):
        print(res)
    else:
        raise Exception("invalid flag:%s" % flag)
    return res
