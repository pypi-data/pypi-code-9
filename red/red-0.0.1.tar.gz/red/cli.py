#!/usr/bin/env python
import sys
import re

def readloop(regex, code):
    r = re.compile(regex)
    for linen in sys.stdin:
        line = linen[:-1]
        match = r.match(line)
        if match is None:
            continue
        if code:
            g = match.groups()
            d = match.groupdict()
            print(eval(code))
        else:
            print(line)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('regex')
    parser.add_argument('--eval', '-e', help='Python code to evaluate, g[0] being the first of the groups if they exist, d["foo"] being the (?P<foo>.*) named group if it exists',
        dest='eval_code')
    args = parser.parse_args()
    readloop(args.regex, args.eval_code)

if __name__ == '__main__':
    main()
