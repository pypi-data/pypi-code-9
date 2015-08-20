"""Popline pops the first line off a file."""

import sys
import subprocess


def main():
    """Main method."""
    if len(sys.argv) < 2:
        raise Exception

    filename = sys.argv[1]
    if len(sys.argv) == 3:
        programme = sys.argv[2]
    else:
        programme = None

    with open(filename, 'r') as fp:
        lines = fp.read()


    lines = lines.split("\n")

    if len(lines) > 0:
        first, rest = lines[0], lines[1:]

        with open(filename, 'w') as fp:
            fp.write("\n".join(rest))

        if programme:
            subprocess.call([programme, first])
        else:
            print first

if __name__ == '__main__':
    main()
