#!/usr/bin/env python

__author__ = 'Xyene'

import argparse
import os
import sys
import subprocess
import math
from version import __version__


def main():
    _parser = argparse.ArgumentParser(prog='sphere2cube', description='''
        Maps an equirectangular (cylindrical projection, skysphere) map into 6 cube (cubemap, skybox) faces.
    ''')
    _parser.add_argument('file_path', nargs='?', metavar='<source>',
                         help='source equirectangular image filename')
    _parser.add_argument('-v', '--version', action='version', version=__version__)
    _parser.add_argument('-r', '--resolution', type=int, default=1024, metavar='<size>',
                         help='resolution for each generated cube face (defaults to 1024)')
    _parser.add_argument('-R', '--rotation', type=int, nargs=3, default=[0, 0, 0], metavar=('<rx>', '<ry>', '<rz>'),
                         help="rotation in degrees to apply before rendering cube faces (z is up)")
    _parser.add_argument('-o', '--output', type=str, default='face_%n_%r', metavar='<path>',
                         help='filename for rendered faces: default is '
                              '"face_%%n_%%r", where %%n is replaced by the face number, and %%r by the resolution')
    _parser.add_argument('-f', '--format', type=str, default='TGA', metavar='<name>',
                         help='format to use when saving faces, i.e. "PNG" or "TGA"')
    _parser.add_argument('-b', '--blender-path', type=str, default='blender', metavar='<path>',
                         help='filename of the Blender executable (defaults to "blender")')
    _parser.add_argument('-t', '--threads', type=int, default=None, metavar='<count>',
                         help='number of threads to use when rendering (1-64)')
    _parser.add_argument('-V', '--verbose', action='store_true',
                         help='enable verbose logging')
    _args = _parser.parse_args()

    rotations = map(lambda x: math.radians(x), _args.rotation)

    if _args.threads and _args.threads not in range(1, 65):
        _parser.print_usage()
        print('sphere2cube: error: too many threads specified (range is 1-64)')
        sys.exit(1)

    if _args.file_path is None:
        _parser.print_help()
        sys.exit(1)

    output = _args.output.replace('%n', '#').replace('%r', str(_args.resolution))
    output = output if os.path.isabs(output) else os.path.join(os.getcwd(), output)

    out = open(os.devnull, 'w') if not _args.verbose else None

    try:
        process = subprocess.Popen(
            [_args.blender_path, '--background', '-noaudio',
             # https://aerotwist.com/tutorials/create-your-own-environment-maps/, CC0
             '-b', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projector.blend'),
             '-o', output, '-F', _args.format, '-x', '1',
             '-P', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'blender_init.py')]
            + (['-t', str(_args.threads)] if _args.threads else [])
            + ['--', _args.file_path, str(_args.resolution), str(rotations[0]), str(rotations[1]), str(rotations[2])],
            stderr=out, stdout=out)
    except:
        print('error spawning blender (%s) executable' % _args.blender_path)
        import traceback

        traceback.print_exc()
        sys.exit(1)
    else:
        process.wait()
        if process.returncode:
            print('blender exited with error code %d' % process.returncode)
            sys.exit(process.returncode)
