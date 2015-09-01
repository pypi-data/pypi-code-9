import argparse as _argparse
import shlex as _shlex
import subprocess as _subprocess


def pdf2png(file_in, file_out):
    """
    Uses `ImageMagick <http://www.imagemagick.org/>`_ to convert an input *file_in* pdf to a *file_out* png. (Untested with other formats.
    """
    command = 'convert -display 37.5 {} -resize 600 -append {}'.format(file_in, file_out)
    _subprocess.call(_shlex.split(command))

if __name__ == '__main__':
    parser = _argparse.ArgumentParser(description=
            'Creates a tunnel primarily for Git.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-i', '--input',
            help='Input file.')
    parser.add_argument('-o', '--output',
            help='Input file.')

    arg = parser.parse_args()

    pdf2png(file_in=arg.input, file_out=arg.output)
