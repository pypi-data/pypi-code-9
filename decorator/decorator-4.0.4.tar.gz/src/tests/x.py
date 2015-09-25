import time
import weakref
from decorator import decorate


def _memoize(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


def memoize(f):
    f.cache = weakref.WeakKeyDictionary()
    return decorate(f, _memoize)


class C(object):
    @memoize
    def f(self):
        time.sleep(1)
        return 1


if __name__ == '__main__':
    instances = [C() for _ in range(10)]
    for instance in instances:
        instance.f()
    del instances
    print C.f.cache
