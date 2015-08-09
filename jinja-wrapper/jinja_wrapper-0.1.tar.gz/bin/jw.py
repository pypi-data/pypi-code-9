#!/usr/bin/env python2

import argparse
import os

from jinja_wrapper.base import JinjaWrapper

# --- Refactor

# --- Parser Helpers
def split_key_value(args):
    _args = args.split(',')
    out = {}
    for kv in _args:
        key, value = kv.split('=')
        out[key] = value
    return out


# --- Main
def get_parser():
    parser = argparse.ArgumentParser(description="wrapper for using jinja")
    parser.add_argument('template',
            metavar='template',
            type=str,
            help='template to use')
    parser.add_argument('--config',
            metavar='<key>=<value>,...',
            type=str,
            help='what configs to use')
    parser.add_argument('--target',
            metavar='<key>=<value>,...',
            type=str,
            help='where to put files',
            default = os.getcwd(),
            )
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    args.config = split_key_value(args.config)
    jw = JinjaWrapper()
    jw.execute(args)

if __name__ == "__main__":
    main()


