from hitchtest.environment import checks
from hitchserve import Service
import subprocess
import os

class RedisService(Service):
    def __init__(self, redis_package, port=16379, **kwargs):
        self.redis_package = redis_package
        self.port = port
        kwargs['command'] = [self.redis_package.server, "--port", str(port)]
        kwargs['log_line_ready_checker'] = lambda line: "The server is now ready to accept connections" in line
        checks.freeports([port, ])
        super(RedisService, self).__init__(**kwargs)

    def cli(self, *args, **kwargs):
        cmd = [self.redis_package.cli, "-p", str(self.port)] + list(args)
        return self.subcommand(*cmd, **kwargs)
