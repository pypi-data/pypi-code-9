#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""
Module generate volumetric data from obj file
"""

import logging
logger = logging.getLogger(__name__)
import argparse
from fileio import readFile
from scipy.spatial import Delaunay
import numpy as np
import glob
import re


def points_to_volume_3D(data3d, points):
    """
    Not fixed yet. Should be better then slice version
    """
    # hack move one point in next slice to make non planar object
    points[0, 2] += 1
    points[-1, 2] += -1

    hull = Delaunay(points)
    X, Y, Z = np.mgrid[:data3d.shape[0], :data3d.shape[1], :data3d.shape[2]]
    grid = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T
    simplex = hull.find_simplex(grid)
    fill = grid[simplex >= 0, :]
    fill = (fill[:, 0], fill[:, 1], fill[:, 2])
    data3d[fill] = 1


def points_to_volume_slice(data3d, points, label):
    """
    Only planar points can be used
    """
    # hack move one point in next slice to make non planar object
    z = points[0, 2]
    points_sl = points[:, :2]

    hull = Delaunay(points_sl)
    X, Y = np.mgrid[:data3d.shape[0], :data3d.shape[1]]
    grid = np.vstack([X.ravel(), Y.ravel()]).T
    simplex = hull.find_simplex(grid)
    fill = grid[simplex >= 0, :]
    fill = (fill[:, 1], fill[:, 0])
    # contours = np.zeros(data3d.shape, np.int8)
    # contours[fill] = 1
    data_slice = data3d[:, :, z]
    data_slice[fill] = label


def slice_ticks_analysis(slice_ticks):
    # TODO implement
    # from collections import Counter
    # slti = np.asarray(slice_ticks)
    # slice_ticks_dif = slti[1:] - slti[:-1]
    # b = Counter(slice_ticks_dif)
    # mc = b.most_common(1) # noqa
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    new_slice_ticks = slice_ticks
    return new_slice_ticks


def read_files_and_make_labeled_image(filesmask, data_offset=None,
                                      data_size=None):

    vs = 0.01
    int_multiplicator = 1 / vs

    filenames = glob.glob(filesmask)
    if data_offset is None or data_size is None:
        data_offset, sz, slice_ticks = find_bbox(filenames,
                                                 return_slice_ticks=True)

    slice_ticks = slice_ticks_analysis(slice_ticks)
    # data_offset = [5600, 6900, 100]
# size cannot be estimated easily
    # size = [400, 400, 300]
    siz = ((np.asarray(sz) / vs).astype(np.int) + 1).tolist()
    size = [siz[0], siz[1], len(slice_ticks)]
    data3d = np.zeros(size)
    for filename in filenames:
        try:
            read_one_file_add_to_labeled_image(filename, data3d, data_offset,
                                               int_multiplicator, slice_ticks)
        except:
            import traceback
            logger.warning(traceback.format_exc())

    # import sed3
    #
    # ed = sed3.sed3(np.transpose(data3d, axes=[2, 0, 1]))
    # ed.show()

    return data3d, None


def find_bbox(filenames, return_slice_ticks=False, slice_axis=2):
    """
    It can be used for slice ticks localization.

    """
    data_min = []
    data_max = []
    slice_ticks = []

    for filename in filenames:
        Vraw, Fraw = readFile(filename)
        V = np.asarray(Vraw)
        data_min.append(np.min(V, axis=0))
        data_max.append(np.max(V, axis=0))
        if return_slice_ticks:
            slice_ticks_one = np.unique(V[:, slice_axis])
            slice_ticks = slice_ticks + slice_ticks_one.tolist()

    mx = np.max(data_max, axis=0)
    mi = np.min(data_min, axis=0)

    if return_slice_ticks:
        return mi, mx, np.unique(slice_ticks).tolist()
    else:
        return mi, mx


def squeeze_slices(V):
    """
    Every two slices are squeezed to one
    """
    # V[V[:, 2] % 2 == 1, 2] += 1
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    V[:, 2] = (V[:, 2] / 2).astype(np.int)
    return V


def read_one_file_add_to_labeled_image(filename, data3d, data_offset,
                                       int_multiplicator, slice_ticks=None,
                                       slice_axis=2,
                                       squeeze_number=2
                                       ):
    """
    squeeze_number
    """

    Vraw, Fraw = readFile(filename)

    # parse filename
    nums = re.findall(r'\d+', filename)
    label = int(nums[0])

    V = np.asarray(Vraw)
    # data_offset = np.min(V, axis=0)
    V = V - data_offset

# TODO rozpracovat do obecnější formy
    # low number of unique numbers in axix - axis of slices
    # slice_axis = argmin  pro kazdou osu z:   len(np.unique(VVV[:,1]))
    # slice_axis = 2

    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    # first_slice_offset = slice_ticks.index(
    #     np.min(unV2) + data_offset[slice_axis])

    # not nice discretization
    V[:, 0] = V[:, 0] * int_multiplicator
    V[:, 1] = V[:, 1] * int_multiplicator

    slice_ticks_0 = np.asarray(slice_ticks) - data_offset[slice_axis]

    slice_indexes = range(0, len(slice_ticks))
    for i in slice_indexes[:-squeeze_number:squeeze_number]:

        in_slice_idx =  \
            (V[:, slice_axis] >= slice_ticks_0[i]) & \
            (V[:, slice_axis] < slice_ticks_0[i + squeeze_number])
        if np.sum(in_slice_idx) > 0:
        # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
            points = V[in_slice_idx, :]
            points[:, 2] = i / squeeze_number
            points = points.astype(np.int)

            if points.shape[0] > 2:
                points_to_volume_slice(data3d, points, label)
                # points_to_volume_3D(data3d, points)
            else:
                print "low number of points", points.shape[0], \
                    " z-level ", points[0, slice_axis]


def reconstruction_old(data3d, V, slice_axis, int_multiplicator, label):
    # TODO use this instead of fallowing fasthack-
    # to be sure not loosing information
    unV2, invV2 = np.unique(V[:, slice_axis], return_inverse=True)

    first_slice_offset_old = unV2[0] / (unV2[1] - unV2[0])
    logger.debug('first_slice_offset ' + str(unV2[:3]) + ' =    ' +
                 str(first_slice_offset_old)
                 )

    # only every second slice is counted. This is why is there /2
    V[:, 2] = invV2 + np.int(first_slice_offset_old / 2)

    V = squeeze_slices(V)

    # not nice discretization
    V[:, 0] = V[:, 0] * int_multiplicator
    V[:, 1] = V[:, 1] * int_multiplicator

    Vint = V.astype(np.int)  # - data_offset

    for slicelevel in np.unique(Vint[:, slice_axis]):
        points = Vint[Vint[:, slice_axis] == slicelevel, :]

        if points.shape[0] > 2:
            points_to_volume_slice(data3d, points, label)
            # points_to_volume_3D(data3d, points)
        else:
            print "low number of points", points.shape[0], \
                " z-level ", points[0, slice_axis]


def write_data3d(data3d, filename):
    import io3d
    dw = io3d.DataWriter()
    dw.Write3DData(data3d, filename, filetype='rawiv',
                   metadata={'voxelsize_mm': [1, 1, 1]})


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

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
        default=None,
        required=True,
        help='output file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    data3d, metadata = read_files_and_make_labeled_image(args.inputfile)

    if args.outputfile is not None:
        write_data3d(data3d, args.outputfile)
