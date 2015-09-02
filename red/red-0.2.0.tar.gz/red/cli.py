#!/usr/bin/env python
import sys
import re

def readloop(regex, code, aggregate=None, f=sys.stdin):
    r = re.compile(regex)
    ag = []
    ad = []
    for linen in f:
        line = linen[:-1]
        match = r.match(line)
        if match is None:
            continue
        if not (code or aggregate):
            print(line)
            continue
        g = match.groups()
        d = match.groupdict()
        if code:
            print(eval(code))
        if aggregate:
            ad += [d]
            ag += [g]
    if aggregate:
        print(eval(aggregate))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('regex')
    parser.add_argument('--eval', '-e', help='Python code to evaluate, g[0] being the first of the groups if they exist, d["foo"] being the (?P<foo>.*) named group if it exists',
        dest='eval_code')
    parser.add_argument('--aggregate', '-a',
        help='aggregate all groups into a list named `ag` and `ad`, and evaluate this code.')
    parser.add_argument('--import', '-i', dest='import_libs',
        help='comma separated modules to import, like `requests` or `json`')
    parser.add_argument('path', nargs='?', help='path to file, leave blank to use stdin')
    args = parser.parse_args()
    if args.path is None:
        readloop(args.regex, args.eval_code, aggregate=args.aggregate)
    else:
        with open(args.path) as f:
            if args.import_libs:
                import importlib
                libs = args.import_libs.split(',')
                for lib in libs:
                    globals()[lib] = importlib.import_module(lib)
            readloop(args.regex, args.eval_code, aggregate=args.aggregate, f=f)


if __name__ == '__main__':
    main()
