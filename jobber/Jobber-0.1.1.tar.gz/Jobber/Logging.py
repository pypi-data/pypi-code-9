__author__ = 'rodak'

import logging

def logger(name, outputPath):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(outputPath)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(handler)
    return logger