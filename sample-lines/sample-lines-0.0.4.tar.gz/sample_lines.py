#!/usr/bin/env python
import argparse, sys
from itertools import count, repeat
from random import randint

def simple_random(n, fp):
    '''
    with replacement

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    '''
    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()
    
    lines_emitted = 0
    for i in count():
        fp.seek(randint(file_start, file_end))
        fp.readline()
        line = fp.readline()
        if len(line) > 0 and line[-1] == '\n':
            yield line
            lines_emitted += 1

        if lines_emitted == n:
            break
        if lines_emitted == 0 and i > 1000:
            raise EnvironmentError('It appears that this file contains no line breaks.')

def systematic(n, fp, repetitions = 1):
    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()
    print(file_start, file_end)
    interval = int((file_end - file_start) / n)
    if interval == 0:
        interval = 1

    offset_adjustments = list(sorted(repeat(randint(0, interval), repetitions)))
    for base_offset in range(file_start, file_end, interval):
        for offset_adjustment in offset_adjustments:
            offset = base_offset + offset_adjustment
            fp.seek(offset)
            fp.readline()
            line = fp.readline()
            
            if len(line) > 0 and line[-1] == '\n':
                yield line

argparser = argparse.ArgumentParser('Randomly select lines from a file.')
argparser.add_argument('file', type = argparse.FileType('r'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to emit')
argparser.add_argument('--method', '-m', choices = ('simple-random', 'systematic'),
                       default = 'simple-random', help = 'Sampling method')
argparser.add_argument('--repeat', '-r', type = int, default = 1,
                       help = 'Number of repetitions for systematic sampling')

def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1

    if args.method == 'systematic':
        if args.repeat < 1:
            sys.stderr.write('You need at least one repetition.\n')
            return 1
        def sample(fp):
            return systematic(args.n, fp, repetitions = args.repeat)
    else:
        def sample(fp):
            return simple_random(args.n, fp)

    for line in sample(args.file):
        try:
            sys.stdout.write(line)
            sys.stdout.flush()
        except (BrokenPipeError, IOError):
            def f(*args, **kwargs):
                pass
            sys.stdout.write = sys.stderr.write = f
            break

if __name__ == '__main__':
    main()
