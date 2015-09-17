from hitchtest.environment import checks
from hitchserve import Service
from os.path import join
import signal
import shutil
import sys

class MemcacheService(Service):
    def __init__(self, memcache_package, port=11211, **kwargs):
        self.memcache_package = memcache_package
        self.port = port
        checks.freeports([port, ])
        kwargs['command'] = [memcache_package.memcached, "-vv", ]
        kwargs['log_line_ready_checker'] = lambda line: "listening" in line
        super(MemcacheService, self).__init__(**kwargs)
