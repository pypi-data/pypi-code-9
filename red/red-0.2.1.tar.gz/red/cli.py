#!/usr/bin/env python
import sys
import re

def readloop(regex, exec_code, eval_code, aggregate=None, exec_aggregate=None, 
        f=sys.stdin):
    r = re.compile(regex)
    ag = []
    ad = []
    for linen in f:
        line = linen[:-1]
        match = r.match(line)
        if match is None:
            continue
        if not any([exec_code, eval_code, aggregate, exec_aggregate]):
            print(line)
            continue
        g = match.groups()
        d = match.groupdict()
        if exec_code:
            exec(exec_code)
        if eval_code:
            print(eval(eval_code))
        if aggregate:
            ad += [d]
            ag += [g]
    if exec_aggregate:
        exec(exec_aggregate)
    if aggregate:
        print(eval(aggregate))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('regex')
    parser.add_argument('--eval', '-e', help='Python code to evaluate, g[0] being the first of the groups if they exist, d["foo"] being the (?P<foo>.*) named group if it exists',
        dest='eval_code')
    parser.add_argument('--exec', '-x', help='Python code to execute (happens before the evaluate and can be chained togther)',
        dest='exec_code')
    parser.add_argument('--aggregate', '-a',
        help='aggregate all groups into a list named `ag` and `ad`, and evaluate this code.')
    parser.add_argument('--exec-aggregate', '-X',
        help='executes before the aggregate, similar to --exec versus --eval')
    parser.add_argument('--import', '-i', dest='import_libs',
        help='comma separated modules to import, like `requests` or `json`')
    parser.add_argument('path', nargs='?', help='path to file, leave blank to use stdin')
    args = parser.parse_args()
    if args.import_libs:
        import importlib
        libs = args.import_libs.split(',')
        for lib in libs:
            globals()[lib] = importlib.import_module(lib)
    if args.path is None:
        readloop(args.regex, args.exec_code, args.eval_code, aggregate=args.aggregate, 
            exec_aggregate=args.exec_aggregate)
    else:
        with open(args.path) as f:
            readloop(args.regex, args.exec_code, args.eval_code, aggregate=args.aggregate, 
                exec_aggregate=args.exec_aggregate, f=f)


if __name__ == '__main__':
    main()
