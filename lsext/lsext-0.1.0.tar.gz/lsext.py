#!/usr/bin/env python3


"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import argparse
import logging
import os
import itertools
import operator

import fswalk

def main(args):
    if not args.dirs:
        args.dirs.append(os.getcwd())

    for i in args.dirs:
        if os.path.isdir(i) and os.access(i, os.F_OK | os.R_OK):
            logging.info("{}: ".format(i))

            all_info = fswalk.walk_directory(
                i,
                get_file_ext if not args.size else get_file_ext_size,
                args.ignore if args.ignore else (),
                args.follow)

            # need two independent generators
            # if we still want to extract size information.
            all_ext_info, all_ext_size_info = itertools.tee(
                all_info) if args.size else (all_info, None)

            all_exts = list(
                map(str.lower, all_ext_info)
                if not args.size else map(
                        str.lower,
                map(operator.itemgetter(0), all_ext_info)))

            unique_exts = sorted(set(all_exts))

            if args.number:
                num = sorted({
                    i:all_exts.count(i) for i in unique_exts
                }.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
                stat_print(num, False)

            elif args.size:
                size = {i:0 for i in unique_exts}

                for i in all_ext_size_info:
                    size[str.lower(i[0])] += i[1]
                size = sorted(
                    size.items(), key=operator.itemgetter(1),
                    reverse=True)
                stat_print(size, str_to_scale[args.human])

            else:
                print((5 * ' ').join(unique_exts))

        else:
            print('could not access: {}\nmay not exist'.format(i))


str_to_scale = {
    'b':1,
    'k':1024,
    'm':1024 * 1024,
    'g':1024 * 1024 * 1024
}

scale_to_str = {
    1:'B',
    1024:'KiB',
    1024 * 1024:'MiB',
    1024 * 1024 * 1024:'GiB'
}


def get_file_ext(file_path):
    return os.path.splitext(file_path)[1]


def get_file_size(filename):
    if os.path.islink(filename):
        return 0

    return os.path.getsize(filename)


def get_file_ext_size(file_path):
    return get_file_ext(file_path), get_file_size(file_path)


def stat_print(source, scale):
    total = sum(map(operator.itemgetter(1), source))

    for i in source:
        print(
            "{:20} {:<20}{:10} {:<10.2%}".format(
                i[0], round(i[1] / scale, 4) if scale else i[1],
                scale_to_str[scale] if scale else '', i[1] / total))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze The Distribution Of File Formats",
        conflict_handler='resolve')

    parser.add_argument(
        'dirs', metavar='dir', nargs='*',
        help='The directory to analyze')
    parser.add_argument(
        '-s', '--size', dest='size', action='store_true',
        help='Analyze size distribution')
    parser.add_argument(
        '-n', '--number', dest='number', action='store_true',
        help='Analyze number distribution')
    parser.add_argument(
        '-h', '--human',
        dest='human', choices=('k', 'm', 'g'), default='b',
        help='Human-readable size in the specified unit')
    parser.add_argument(
        '-f', '--follow', dest='follow', action='store_true',
        help='Follow symbolic links')
    parser.add_argument(
        '-i', '--ignore', dest='ignore', nargs='+',
        help='Ignore the specified directory names')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='turn on verbose mode, -vv for debugging mode')
    parser.add_argument(
        '-V', '--version', action='version', version='Version 0.1')

    return parser.parse_args()


def start_main():
    args = parse_args()

    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG
        }[args.verbose % 3])

    sys.exit(main(args))


if __name__ == '__main__':
    start_main()
