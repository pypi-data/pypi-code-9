#!/usr/bin/env python
from __future__ import print_function
from itertools import product, combinations

import sys
from path import path
import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform
from prody import parsePDBStream
from sblu.ft import (read_rotations, read_ftresults,
                     apply_ftresults_atom_group)
from sblu.util import add_atom_selection_arguments

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

try:
    xrange
except NameError:
    xrange = range


def pwrmsd(lig, condensed=False):
    nftresults = lig.numCoordsets()

    condensed_dists = pdist(lig._getCoordsets().reshape(nftresults, -1),
                            'sqeuclidean')
    np.divide(condensed_dists, lig.numAtoms(), condensed_dists)
    np.sqrt(condensed_dists, condensed_dists)
    if not condensed:
        return squareform(condensed_dists)
    return condensed_dists


def interface(rec_coords, lig_coords, interface_d):
    dists = cdist(rec_coords, lig_coords, 'sqeuclidean')
    indices = np.any(dists < (interface_d*interface_d), axis=0).nonzero()[0]
    return indices


def interface_pwrmsd(rec, lig,
                     interface_d=10.0, condensed=False):
    transformed = lig._getCoordsets()
    nftresults = lig.numCoordsets()

    interfaces = [interface(rec._getCoords(), coords, 10.0) for
                  coords in transformed]

    dists = np.zeros((nftresults, nftresults), dtype=np.float64)
    for i in xrange(nftresults):
        for j in xrange(i, nftresults):
            combined_interface = np.union1d(interfaces[i], interfaces[j])
            if len(combined_interface) == 0:
                d = -1
            else:
                d = rmsd(transformed[i][combined_interface],
                         transformed[j][combined_interface])
            dists[i, j] = dists[j, i] = d

    if condensed:
        return squareform(dists)
    return dists


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType

    parser = ArgumentParser(
        description="Calculate pairwise RMSDs.",
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("--sort-ftresults", action="store_true", default=False)
    parser.add_argument("--nftresults", "-n", type=int, default=1000,
                        help="Number of ftresults to use")

    parser.add_argument("--rec", help="Receptor pdb file.")
    parser.add_argument("--interface", action="store_true", default=False)
    parser.add_argument("--interface-radius", type=float, default=10.0)

    parser.add_argument("--output", "-o", type=FileType('w'),
                        help="Write output to file (default: stdout)")

    parser.add_argument("ligfile", help="Ligand pdb file.")
    parser.add_argument("ftfile", help="FT results file from docking.")
    parser.add_argument("rotprm", help="Rotations file used in docking.")
    add_atom_selection_arguments(parser)

    args = parser.parse_args()

    with open(args.ligfile) as ligf:
        lig = parsePDBStream(ligf)

    ftresults = read_ftresults(args.ftfile, limit=args.nftresults)
    if args.sort_ftresults:
        ftresults.sort(order='E', kind='mergesort')  # only mergesort is stable

    rotations = read_rotations(args.rotprm)

    center = np.mean(lig.getCoords(), axis=0)

    if args.only_CA:
        lig = lig.calpha
    elif args.only_backbone:
        lig = lig.backbone
    elif args.only_selection is not None:
        lig = lig.select(args.only_selection)

    transformed = apply_ftresults_atom_group(lig, ftresults, rotations,
                                             center=center)

    if args.interface:
        with open(args.rec) as recf:
            rec = parsePDBStream(recf)

        pairwise_dists = interface_pwrmsd(rec, transformed,
                                          interface_d=10.0, condensed=False)
    else:
        pairwise_dists = pwrmsd(transformed)

    ofile = args.output
    if ofile is None:
        ofile = "clustermat.{0}".format(path(args.ftfile).basename())

    for rmsd in pairwise_dists.flat:
        print("{:.2f}".format(rmsd), file=args.output)
