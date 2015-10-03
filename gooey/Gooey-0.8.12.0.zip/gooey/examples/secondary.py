from argparse import ArgumentParser
import json
import os
from gooey import Gooey, GooeyParser


@Gooey(program_name="Create Quarterly Marketing Report")
def parse_args():
    """ Use GooeyParser to build up the arguments we will use in our script
    """

    defaults = {}


    parser = ArgumentParser(description='Create Quarterly Marketing Report')
    parser.add_argument('data_directory',
                        action='store',
                        default=defaults.get('data_directory', ''),
                        help="Source directory that contains Excel files")
    args = parser.parse_args()
    return args


def load_defaults():
  if os.path.isfile("gui_args.json"):
      with open("gui_args.json") as data_file:
          return json.load(data_file)
  return

if __name__ == '__main__':
    parse_args()
