import logging
import inspect
import argparse
import os


class Keywords(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


class IndentFormatter(logging.Formatter):
    def __init__( self, fmt=None, datefmt=None, indent_offset=6):
        if fmt is None:
            fmt = '%(indent)s==========================================================\n%(indent)s%(levelname)s - %(name)s:%(funcName)s:%(lineno)d\n%(indent)s%(message)s'

        super(IndentFormatter, self).__init__(fmt=fmt, datefmt=datefmt)
        #  print type(len(inspect.stack()))
        #  print type(indent_offset)
        self.baseline = len(inspect.stack()) + indent_offset

    def format( self, rec ):
        stack = inspect.stack()
        stackdepth = len(stack)
        stackdiff = stackdepth - self.baseline
        rec.indent = '\t' * stackdiff
        #  rec.function = stack[8][3]
        out = logging.Formatter.format(self, rec)
        del rec.indent
        #  del rec.function
        return out


# ================================
# Access environment variables
# ================================
def checkvar(envvar):
    try:
        value = os.environ[envvar]
    except:
        value = None
    # print(value)
    return value


# Email variable class
class emailprefs:
    # print(requested)
    # print(value)
    # raise argparse.ArgumentTypeError('hi')
    """Preferences for email notification."""
    def __init__(self, requested=False, environvar=None, value=None):
        self.requested = requested
        self.environvar = environvar
        if value is None:
            self.value = checkvar(environvar)
        else:
            self.value = value
        if self.value is None:
            self.value = os.environ['PHYSICS_USER']
            print('Using current fphysics login: ' + self.value)

        # raise ValueError('problem')


# Adds action to load email from $NOTIFY_EMAIL if possible
class note_address(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print getattr(namespace, self.dest).environvar
        # print values
        if values is None:
            out = emailprefs(True, getattr(namespace, self.dest).environvar)
        else:
            out = emailprefs(True, getattr(namespace, self.dest).environvar, values)
        setattr(namespace, self.dest, out)
