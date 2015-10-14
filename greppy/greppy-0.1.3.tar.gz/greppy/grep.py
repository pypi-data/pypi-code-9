# -*- coding: utf-8 -*-
import argparse
import sys
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ignore-case", action="store_true")
    parser.add_argument("-n", "--line-number", action="store_true")
    parser.add_argument("-H", "--with-filename", action="store_true")
    parser.add_argument("pattern", type=str)
    parser.add_argument(
        "files", nargs="*", default=[sys.stdin], type=argparse.FileType("r"))
    return parser.parse_args()


def main(args):
    flags = re.IGNORECASE if args.ignore_case else 0
    for file_in in args.files:
        for index, line in enumerate(file_in):
            if re.search(args.pattern, line, flags):
                line = "{}:{}".format(
                    index, line.strip()) if args.line_number else line
                line = "{}:{}".format(
                    file_in.name, line.strip()) if args.with_filename else line
                print line.strip()
