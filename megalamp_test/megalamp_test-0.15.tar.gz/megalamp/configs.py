# encoding=utf-8

import argparse


argparser = argparse.ArgumentParser(
    description="The BF Lamp.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

argparser.add_argument(
    "-H", "--host",
    default='127.0.0.1',
    help="specify server host"
)

argparser.add_argument(
    "-P", "--port",
    default=9999,
    help="specify server port",
)

argparser.add_argument(
    "-l", "--logfile",
    help="specify file for logging",
)


class LazyConfig(argparse.Namespace):
    def __getattr__(self, name):
        if not self.__dict__:
            argparser.parse_args(namespace=self)
            return getattr(self, name)
        raise AttributeError(name)

config = LazyConfig()
