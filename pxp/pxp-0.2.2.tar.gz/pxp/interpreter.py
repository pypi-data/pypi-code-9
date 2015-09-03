"""This module contains classes and methods related to interpreting and executing PXP programs."""

from ._interpreter import Interpreter, Resolver


def _main():
  """Handles command line interaction."""
  args = _parse_args()
  args.func(args)


def _parse_args():
  """Parses command line arguments."""
  import sys
  from argparse import ArgumentParser

  arg_parser = ArgumentParser(description="Compile or run pxp files")
  subparsers = arg_parser.add_subparsers()

  compile_parser = subparsers.add_parser("compile", description="Compile a pxp program")
  compile_parser.add_argument("in_filename",
                              nargs="?",
                              help="The file to compile. If not given you will be prompted to "
                                   "enter the program on the command line.")
  compile_parser.add_argument("out_filename",
                              help="The file to which to output the byte code. If the file has an "
                                   "extension other than .pxpc, that extension will be added to "
                                   "the filename that is given before output.")
  compile_parser.set_defaults(func=_compile)

  execute_parser = subparsers.add_parser("exec", description="Execute a pxp program")
  execute_parser.add_argument("filename",
                              nargs="?",
                              help="The file to execute. This can be a .pxp file, which will be "
                                   "compiled and executed, or a .pxpc file which will be executed "
                                   "directly. If not given you will be prompted to enter the "
                                   "program on the command line")
  execute_parser.set_defaults(func=_exec)

  args = arg_parser.parse_args()

  if hasattr(args, "func"):
    return args
  else:
    arg_parser.print_help()
    sys.exit(1)


def _compile(args):
  """Compile a pxp program."""
  import os
  import pickle
  from pxp.compiler import Compiler

  if args.in_filename:
    with open(args.in_filename) as rf:
      source = rf.read()
  else:
    source = _read_source()

  filename, ext = os.path.splitext(args.out_filename)
  if ext != ".pxpc":
    out_filename = args.out_filename + ".pxpc"
  else:
    out_filename = args.out_filename

  byte_code = Compiler(source).compile()
  with open(out_filename, "wb") as wf:
    pickle.dump(byte_code, wf)


def _exec(args):
  """Execute a pxp program."""
  import os
  from pxp.compiler import Compiler

  source = None
  byte_code = None

  if args.filename:
    _, ext = os.path.splitext(args.filename)
    if ext == ".pxpc":
      import pickle

      with open(args.filename, "rb") as rf:
        byte_code = pickle.load(rf)
    else:
      with open(args.filename, "r") as rf:
        source = rf.read()
  else:
    source = _read_source()

  if source:
    byte_code = Compiler(source).compile()

  print(Interpreter().execute(byte_code))


def _read_source(term="\\eof"):
  """Read a pxp program from the command line."""
  lines = []

  print("Enter the program then type {0} on its own line:".format(term))
  line = input("> ")
  while line != term:
    lines.append(line)
    line = input("> ")

  return "\n".join(lines)


if __name__ == "__main__":
  _main()
