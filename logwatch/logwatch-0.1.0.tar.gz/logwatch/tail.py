#!/usr/bin/env python
import os

AVG_LINE_LEN = 256

def tail(path=None, ct=1, avg_line_len=AVG_LINE_LEN):
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(path):
        return None
    size = os.path.getsize(path)
    if size == 0:
        return None
    seek = 1
    lines = []
    i = 1
    while len(lines) < ct and seek > 0:
        min_seek = avg_line_len * ct * i
        seek = max(size - min_seek, 0)
        with open(path) as f:
            f.seek(seek)
            lines = f.readlines()
        if len(lines) < ct:
            i += 1
    neg_ct = -1 * ct
    return [x[:-1] for x in lines[neg_ct:]]

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='pytail')
    parser.add_argument('path', help='path to read from')
    parser.add_argument('--count', '--ct', '-c', type=int, default=10,
        dest='ct',
        help='number of lines to pull (default: %(default)s)')
    parser.add_argument('--average-line-len', '--avg', '-a', type=int,
        dest='avg_line_len',
        default=AVG_LINE_LEN, help='average line length (default %(default)s)')
    args = parser.parse_args()
    for line in tail(**dict(args._get_kwargs())):
        print(line)

if __name__ == '__main__':
    main()
