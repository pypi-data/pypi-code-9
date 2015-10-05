#!/usr/bin/env python
from __future__ import print_function
from prody import parsePDB, parsePDBStream
import numpy as np
from scipy.spatial.distance import cdist
from sblu.ft import (read_rotations, read_ftresults,
                     apply_ftresults_atom_group)
from sblu.util import add_atom_selection_arguments

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


def rmsd(lig, lig_crys, interface_radius=9.0, rec_coords=None):
    assert(len(lig) == len(lig_crys))

    if rec_coords is not None:
        r_sq = interface_radius*interface_radius
        dists = cdist(rec_coords, lig, 'sqeuclidean')
        interface = np.any(dists < r_sq, axis=0).nonzero()[0]
        lig = lig[interface]
        lig_crys = lig_crys[interface]

    delta = lig - lig_crys
    np.multiply(delta, delta, delta)
    return np.sqrt(np.sum(delta)/len(lig))


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(
        description="Calculate RMSDs of poses from an FT file to a target structure.")

    parser.add_argument("--sort-ftresults", action="store_true", default=False)
    parser.add_argument("--nftresults", "-n", type=int, default=None,
                        help="Number of ftresults to use. (Default: all)")

    parser.add_argument("--rec", default=None,
                        help="Receptor file if using interface mode.")
    parser.add_argument("--interface-only", action='store_true', default=False,
                        help="Only use inteface atoms. Requires --rec.")
    parser.add_argument("--interface-radius", type=float, default=10.0,
                        help="Radius around receptor to consider.")

    parser.add_argument("--output", "-o", type=FileType('w'),
                        help="Write output to file (default: stdout)")

    parser.add_argument("ligfile", type=FileType('r'),
                        help="Ligand file to calculate RMSD for.")
    parser.add_argument("lig_crys", type=FileType('r'),
                        help="Ligand file to calculate RMSD for.")
    parser.add_argument("ftfile", help="FT results file from docking.")
    parser.add_argument("rotprm", help="Rotation file used in docking.")
    add_atom_selection_arguments(parser)

    args = parser.parse_args()

    lig = parsePDBStream(args.ligfile)
    lig_crys = parsePDBStream(args.lig_crys)

    ftresults = read_ftresults(args.ftfile, limit=args.nftresults)
    if args.sort_ftresults:
        ftresults.sort(order='E', kind='mergesort')  # only mergesort is stable

    rotations = read_rotations(args.rotprm)

    transformed = apply_ftresults_atom_group(lig, ftresults, rotations)

    if args.only_CA:
        transformed = transformed.calpha
    elif args.only_backbone:
        transformed = transformed.backbone
    elif args.only_selection is not None:
        transformed = transformed.select(args.only_selection)

    rec_coords = None
    if args.rec and args.interface_only:
        rec = parsePDB(args.rec)
        rec_coords = rec.getCoords()

    if args.only_CA:
        lig_coords = lig.select("name CA").getCoords()
        lig_crys = lig_crys.select("name CA").copy()
    else:
        lig_coords = lig.getCoords()

    lig_crys_coords = lig_crys.getCoords()

    for coords in transformed._getCoordsets():
        rms = rmsd(coords, lig_crys_coords,
                   args.interface_radius, rec_coords)
        print("{:.2f}".format(rms))
