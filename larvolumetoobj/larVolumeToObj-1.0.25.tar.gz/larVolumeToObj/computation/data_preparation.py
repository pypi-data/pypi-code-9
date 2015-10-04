#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import argparse

import sys

import numpy as np
import io3d
import io3d.datareader
import io3d.datawriter
import sed3

def preparedata(inputfile, outputfile='prepared.pklz', crop=None, threshold=None,
                visualization=False, zero_border=0, label=2):
    """

    :param inputfile: path to input file or directory, See io3d library for available file formats.
    :param outputfile: path to output file
    :param crop: crop parameters with fallowing format [[minX, maxX], [minY, maxY], [minZ. maxZ]]
    :param threshold:  set threshold for data
    :param visualization: set true to show visualization
    :param zero_border: data border can be set to zero. zero_border. Default is 0
    :param label: set segmentation output label. Default is 2
    :return:
    """
    datap = io3d.datareader.read(inputfile, dataplus_format=True)
    if crop is not None:
        datap['data3d'] = datap['data3d'][crop[0][0]:crop[0][1], crop[1][0]:crop[1][1], crop[2][0]:crop[2][1]]
        if 'segmentation' in datap.keys():
            datap['segmentation'] = datap['segmentation'][crop[0][0]:crop[0][1], crop[1][0]:crop[1][1], crop[2][0]:crop[2][1]]

    if threshold is not None:
        datap['segmentation'] = (datap['data3d'] > threshold).astype(np.uint8) * label
    if visualization:
        ed = sed3.sed3(datap['data3d'], contour=datap['segmentation'])
        ed.show()
    if zero_border > 0:
        datap['segmentation'][:zero_border, :, :] = 0
        datap['segmentation'][:, :zero_border, :] = 0
        datap['segmentation'][:, :, :zero_border] = 0
        datap['segmentation'][-zero_border:, :, :] = 0
        datap['segmentation'][:, -zero_border:, :] = 0
        datap['segmentation'][:, :, -zero_border:] = 0
    # datap['segmentation'][datap['segmentation'] > 0] = label
    io3d.datawriter.write(datap, outputfile)
#



def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-o', '--outputfile',
        default='out.pklz',
        help='output file'
    )
    # parser.add_argument(
    #     '-bf', '--borderfile',
    #     default=None,
    #     help='input file'
    # )
    parser.add_argument(
        '-t', '--threshold',
        default=None,
        help='selected threshold for unlabeled data',
        type=int
    )
    parser.add_argument(
        '-c', '--crop',
        default=None, # [2, 2, 2],
        type=int,
        metavar='N',
        nargs='+',
        help='Crop parameters. Six integers expected: minX maxX minY maxY minZ maxZ'
    )
    parser.add_argument(
        '-v', '--visualization', action='store_true',
        help='Visualization')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()
    if args.debug:
        ch.setLevel(logging.DEBUG)

    crop=None
    if args.crop is not None:
        crop = np.asarray(args.crop).reshape([3, 2])

    preparedata(args.inputfile, args.outputfile, crop=crop,
                threshold=args.threshold, visualization=args.visualization)


if __name__ == "__main__":
    main()
