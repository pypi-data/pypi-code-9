try:
    from PyQt5 import QtSvg, QtGui
except ImportError:
    from PyQt4 import QtSvg, QtGui

import argparse
import os

__author__ = 'pierre'


def merge_svg_png():

    parser = argparse.ArgumentParser(description='Krita .kra file batch processing')

    parser.add_argument(
            '-p', '--png'
        )

    parser.add_argument(
            '-s', '--svg'
    )

    parser.add_argument(
            '-o', '--out', required=True
    )

    parser.add_argument(
        '-w', '--workdir', default=os.curdir
    )


    args = parser.parse_args()

    if args.png:
        png = os.path.join(os.path.abspath(os.curdir), args.png)

    if args.svg:
        svg = os.path.join(os.path.abspath(os.curdir), args.svg)

    if args.workdir:
        os.chdir(args.workdir)

    painter = QtGui.QPainter()

    im = QtGui.QImage()
    im.load(png)

    painter.begin(im)

    render = QtSvg.QSvgRenderer()
    render.load(svg)
    render.render(painter)

    painter.end()
    im.save(args.out)

if __name__ == '__main__':
    merge_svg_png()