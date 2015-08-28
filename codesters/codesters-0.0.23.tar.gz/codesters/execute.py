#!/usr/bin/python
import run, example, sys, argparse

def execute(filename):
    run.run(filename)

def execute_example(filename):
    example.run(filename)

# Standard boilerplate to call the main() function to begin
# the program.
def runner():
    parser = argparse.ArgumentParser(
                                    description = "Runs codesters files",
                                    #epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    #fromfile_prefix_chars = '@'
                                    )
    parser.add_argument(
                      "filename",
                      help = "pass filename to the program",
                      metavar = "filename")
    parser.add_argument(
                      "-e",
                      "--example",
                      help="run codesters example",
                      action="store_true")
    args = parser.parse_args()

    if args.example:
        execute_example(args.filename)
    else:
        execute(args.filename)