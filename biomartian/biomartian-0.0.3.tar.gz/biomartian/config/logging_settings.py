import sys

import logging



def set_up_logging(level=logging.INFO):

    logging.root.setLevel(level)

    logging.basicConfig(level=logging.INFO, format='%(message)s (File: %(module)s, Log level: %(levelname)s, Time: %(asctime)s )',
                        datefmt='%a, %d %b %Y %H:%M:%S', stream=sys.stderr)
