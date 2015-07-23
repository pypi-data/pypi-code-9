import sys


def print_err(*args):
    """\
    Printing to stderr.
    """
    sys.stderr.write(' '.join(map(str,args)) + '\n')

