"""
Implements the command line interface:
argument parsing and the minimal logic required to run a search
and output it in a useful form.
"""

import argparse
import json
import sys

try:
    import multiprocessing
    NUM_CPUS = multiprocessing.cpu_count()
except ImportError:
    NUM_CPUS = 1

from . import comms
from . import search

parser = argparse.ArgumentParser()
# This (obviously) is the only arg you can't specify in the config file.
parser.add_argument('-c', '--config-file')

parser.add_argument('--initial-binary', default='cat $initial-file')
parser.add_argument('--initial-file', default='initial.json')
parser.add_argument('--mutate-binary', default='./mutate')
parser.add_argument('--score-binary', default='./score')

parser.add_argument('--beam-width', type=int, default=5)
parser.add_argument('--expand-mantissa', type=float, default=1.25)
parser.add_argument('--expand-multiplier', type=int, default=3)
parser.add_argument('--target', default='max')

parser.add_argument('--num-iterations', type=int, default=50)
parser.add_argument('--parallelism', type=int, default=NUM_CPUS)

class ParserError(ValueError):
    pass

def parse_file(f):
    for line in f:
        # Ignore comments and blank lines.
        if line.startswith('#') or not line.strip():
            continue
        line = line.rstrip('\n')
        try:
            key, value = line.split(' = ', 1)
        except ValueError:
            raise ParserError('Invalid config line: %r' % line)
        yield key, value

def parse_args():
    # Read arguments from the command line.
    args = parser.parse_args()
    if args.config_file is not None:
        # If -c is specified, read from that file.
        file_argv = []
        with open(args.config_file) as f:
            for key, value in parse_file(f):
                file_argv.append('--' + key)
                file_argv.append(value)
        # Parse the file arguments with argparse.
        file_args = parser.parse_args(file_argv)
        # And then override with the command-line arguments.
        args = parser.parse_args(namespace=file_args)

    # Hack for convenience.
    args.initial_binary = args.initial_binary.replace(
        '$initial-file',
        args.initial_file,
    )
    return args

def main():
    args = parse_args()

    states = search.get_initial_states(args.initial_binary)

    comms.install_signal_handler()
    mutator = comms.Job(args.mutate_binary, args.parallelism, shell=True)
    scorer = comms.Job(args.score_binary, args.parallelism, shell=True)

    searcher = search.Searcher(
        states, mutator, scorer,
        args.beam_width,
        args.expand_mantissa,
        args.expand_multiplier,
        args.target,
    )

    for _ in range(args.num_iterations):
        scores = searcher.step()
        print>>sys.stderr, ', '.join(
            '%.2f' % score for score, _ in scores
        )

    for state in searcher.best:
        print json.dumps(state)

if __name__ == '__main__':
    main()
