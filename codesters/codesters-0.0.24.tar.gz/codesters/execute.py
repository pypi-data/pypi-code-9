#!/usr/bin/python
import run, example, argparse

def execute(filename):
    run.run(filename)

def execute_example(filename):
    example.run(filename)

# Standard boilerplate to call the main() function to begin
# the program.
def runner():
    parser = argparse.ArgumentParser(
                                    usage = "This command runs codesters files. A default command would be as follows:\n\n codesters <options> filename\n",
                                    description = "Options: \n -e <examplename> runs a pre-made example codesters file",
                                    epilog = "Please try again!",

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