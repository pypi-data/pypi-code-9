import logging as _logging
import inspect as _inspect
__all__ = ['mylogger', 'log']


def mylogger(filename, indent_offset=7):
    """
    Sets up logging to *filename*.debug.log, *filename*.log, and the terminal. *indent_offset* attempts to line up the lowest indent level to 0.
    """
    logger = _logging.getLogger()
    logger.setLevel(_logging.DEBUG)

    fmtr         = IndentFormatter(indent_offset=indent_offset)
    fmtr_msgonly = IndentFormatter('%(indent)s%(message)s')

    debugh = _logging.FileHandler(filename='{}_debug.log'.format(filename), mode='w')
    debugh.setLevel(_logging.ERROR)
    debugh.setFormatter(fmtr_msgonly)
    logger.addHandler(debugh)

    ch = _logging.StreamHandler()
    ch.setLevel(_logging.DEBUG)
    ch.setFormatter(fmtr_msgonly)
    logger.addHandler(ch)

    fh = _logging.FileHandler(filename='{}.log'.format(filename), mode='w')
    fh.setLevel(1)
    fh.setFormatter(fmtr)
    logger.addHandler(fh)

    return logger


def log(logger, level):
    def log(msg):
        return logger.log(level=level, msg=msg)
    return log


class IndentFormatter(_logging.Formatter):
    def __init__( self, fmt=None, datefmt=None, indent_offset=6):
        if fmt is None:
            fmt = '%(indent)s==========================================================\n%(indent)s%(levelname)s - %(name)s:%(funcName)s:%(lineno)d\n%(indent)s%(message)s'

        super(IndentFormatter, self).__init__(fmt=fmt, datefmt=datefmt)
        self.baseline = len(_inspect.stack()) + indent_offset

    def format( self, rec ):
        stack = _inspect.stack()
        stackdepth = len(stack)
        stackdiff = stackdepth - self.baseline
        rec.indent = '\t' * stackdiff
        #  rec.function = stack[8][3]
        out = _logging.Formatter.format(self, rec)
        del rec.indent
        #  del rec.function
        return out
