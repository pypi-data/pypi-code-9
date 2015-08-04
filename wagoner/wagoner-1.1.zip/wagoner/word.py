#! /usr/bin/env python3

"""
The word module generate, from a given table, a (set of) random words.
"""

import argparse
import pickle
from wagoner.utils import *
from wagoner.table import Table
from wagoner.tree import Tree


def process_arguments():
    """
    Process the command line arguments. The arguments are:
     * the table to generate random from;
     * -l (or --length) for the length of generated words (default: 10);
     * -p (or --prefix) for the maximum of prefixes to consider (default: 0);
     * -c (or --count) for the number of words to generate (default: 10);
     * -s (or --start) for generating only words starting in table;
     * -e (or --end) for generating only words ending in table;
     * -f (or --flatten) if the table must be flattened before generation.
    """
    parser = argparse.ArgumentParser(description="Generate random words from "
                                                 "the given content",
                                     epilog="This script can generate random"
                                            "words from tables, trees or "
                                            "texts. If a tree is given, "
                                            "the length of the generated "
                                            "words depend on the tree. If a "
                                            "table is given, the table is "
                                            "used to generate words, except "
                                            "if --end option is given. If a "
                                            "text is given, "
                                            "the corresponding table is "
                                            "built, and also the tree if "
                                            "needed.")
    parser.add_argument("content", help="the content")
    parser.add_argument("--length", "-l", type=nonzero_natural, default=10,
                        dest="length", help="the length of generated words "
                                            "(default: 10)")
    parser.add_argument("--prefix", "-p", type=natural, default=0,
                        dest="prefix", help="if not 0, the maximum length of "
                                            "prefixes to consider when "
                                            "choosing the next character "
                                            "(default: 0)")
    parser.add_argument("--count", "-c", type=natural, default=10,
                        dest="count", help="the number of words to generate "
                                           "(default: 10)")
    parser.add_argument("--start", "-s", action="store_true", default=False,
                        dest="start", help="only starting words")
    parser.add_argument("--end", "-e", action="store_true", default=False,
                        dest="end", help="only ending words")
    parser.add_argument("--flatten", "-f", action="store_true", default=False,
                        dest="flatten", help="flatten the table")
    return parser.parse_args()

if __name__ == "__main__":
    args = process_arguments()
    try:
        with open(args.content, "rb") as content_file:
            content = pickle.load(content_file)
    except pickle.UnpicklingError:
        with open(args.content, "r") as text_file:
            content = Table.from_words(extract_words(text_file),
                                       prefix=args.prefix,
                                       flatten=args.flatten)
    if args.end and isinstance(content, Table):
        content = Tree.from_table(content, args.length, prefix=args.prefix,
                                  flatten=args.flatten)
    for _ in range(args.count):
        print(content.random_word(args.length, prefix=args.prefix,
                                  start=args.start, end=args.end,
                                  flatten=args.flatten))
