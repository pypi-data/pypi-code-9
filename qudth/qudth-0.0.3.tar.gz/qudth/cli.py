import argparse, sys
from statistics import StatisticsError

from sparkprob.sparkprob import sparkprob

from .qudth import qudth

def sparkline(xs):
    total = float(sum(xs))
    return sparkprob((x/total for x in xs), minimum = -0.1).decode('utf-8')

def cli():
    args = argparser.parse_args()
    stats = qudth(args.file, bins = args.bins, n = args.n)
    if stats['min'] == stats['max']:
        sys.stdout.write(boring_template % (args.n, args.file.name, stats['min']))
        return

    stat_keys = ['min', 'median', 'max']

    places = len(str(stats['max']))
    formatstring = '%0' + str(places) + 'd'
    str_stats = {k:(formatstring % (stats[k])) for k in stat_keys}

    n_spaces = 2 * len(stats['histogram']) - 3 * places
    str_stats['delimiter_left'] = ' ' * int(n_spaces / 2)
    str_stats['delimiter_right'] = ' ' * (n_spaces - len(str_stats['delimiter_left']))
    bottom = '%(min)s%(delimiter_left)s%(median)s%(delimiter_right)s%(max)s' % str_stats

    template_args = {
        'filename': args.file.name,
        'n': args.n,
        'histogram': sparkline(stats['histogram']),
        'bottom': bottom,
    }
    sys.stdout.write(interesting_template % template_args)


argparser = argparse.ArgumentParser('Estimate the length of a line in a file.')
argparser.add_argument('file', type = argparse.FileType('r'))
argparser.add_argument('--bins', type = int, default = 20)
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n')

boring_template = 'All %d lines sampled from %s have length %d.\n'
interesting_template = '''
%(histogram)s
%(bottom)s
Lengths of %(n)d lines in %(filename)s
(simple random sample with replacement)
'''
