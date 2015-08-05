import collections
import argparse
import os


def filter_tag(arg):
    """ Parses a --filter-tag argument """
    try:
        strip_len = len('Key=')
        key, value = arg[strip_len:].split(',Value=', 1)
        return key, value
    except:
        msg = 'Invalid --filter-tag argument: {}'
        raise argparse.ArgumentTypeError(msg.format(arg))


def file_arg(arg):
    """
    Parses a file argument, i.e. starts with file://
    """
    prefix = 'file://'

    if arg.startswith(prefix):
        return os.path.abspath(arg[len(prefix):])
    else:
        msg = 'Invalid file argument "{}", does not begin with "file://"'
        raise argparse.ArgumentTypeError(msg.format(arg))


ParameterArgument = collections.namedtuple(
    'ParameterArgument',
    ['value', 'kind']
)


def parameter_arg(arg):
    try:
        return ParameterArgument(value=file_arg(arg), kind='file')
    except argparse.ArgumentTypeError:
        return ParameterArgument(value=arg, kind='cli')
