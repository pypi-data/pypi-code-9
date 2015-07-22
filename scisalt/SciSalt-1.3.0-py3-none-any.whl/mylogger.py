import logging
__all__ = ['mylogger', 'log']

from . import classes


def mylogger(filename, indent_offset=7):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fmtr         = classes.IndentFormatter(indent_offset=indent_offset)
    fmtr_msgonly = classes.IndentFormatter('%(indent)s%(message)s')

    debugh = logging.FileHandler(filename='{}_debug.log'.format(filename), mode='w')
    debugh.setLevel(logging.ERROR)
    debugh.setFormatter(fmtr_msgonly)
    logger.addHandler(debugh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmtr_msgonly)
    logger.addHandler(ch)

    fh = logging.FileHandler(filename='{}.log'.format(filename), mode='w')
    fh.setLevel(1)
    fh.setFormatter(fmtr)
    logger.addHandler(fh)

    return logger


def log(logger, level):
    def log(msg):
        return logger.log(level=level, msg=msg)
    return log
