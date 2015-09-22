#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from babel.messages.frontend import CommandLineInterface

APP_NAME = "rhizom"

parser = ArgumentParser()
#subparsers = parser.add_subparsers()
#parser_init = subparsers.add_parser("init")
#parser_init.add_argument("lang")

parser.add_argument("command", choices=["init", "update", "compile"])
parser.add_argument("lang", nargs="?")

args = parser.parse_args()
pybabel = CommandLineInterface()

if args.command == "init":
    if not args.lang:
        parser.error("missing language")
    pybabel.run(["pybabel", "extract", "-F", "babel.cfg",
                 "-k", "lazy_gettext", "-o", "messages.pot", APP_NAME])
    pybabel.run(["pybabel", "init", "-i", "messages.pot", "-l", args.lang,
                 "-d", os.path.join(APP_NAME, "translations")])
    os.remove("messages.pot")

elif args.command == "update":
    pybabel.run(["pybabel", "extract", "-F", "babel.cfg",
                 "-k", "lazy_gettext", "-o", "messages.pot", APP_NAME])
    pybabel.run(["pybabel", "update", "-i", "messages.pot",
                 "-d", os.path.join(APP_NAME, "translations")])
    os.remove("messages.pot")

elif args.command == "compile":
    pybabel.run(["pybabel", "compile", "--statistics",
                 "-d", os.path.join(APP_NAME, "translations")])
