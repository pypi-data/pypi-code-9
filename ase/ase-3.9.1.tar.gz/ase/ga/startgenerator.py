""" Methods for generating new random starting candidates. """
from random import shuffle
import numpy as np
from ase import Atoms
from ase.ga.utilities import get_mic_distance


def random_pos(box):
    """ Returns a random position within the box
         described by the input box. """
    p0 = box[0]
    vspan = box[1]
    r = np.random.random((1, len(vspan)))
    pos = p0.copy()
    for i in range(len(vspan)):
        pos += vspan[i] * r[0, i]
    return pos


class StartGenerator(object):

    """ Class used to generate random starting candidates.
        The candidates are generated by iteratively adding in
        one atom at a time within the box described.

        Parameters:

        slab: The atoms object describing the super cell to
        optimize within.
        atom_numbers: A list of the atomic numbers that needs
        to be optimized.
        closed_allowed_distances: A dictionary describing how
        close two atoms can be.
        box_to_place_in: The box atoms are placed within.  The format
        is [p0, [v1, v2, v3]] with positions being generated as p0 +
        r1 * v1 + r2 * v2 + r3 + v3. Default value: [[0, 0, 0],
        [Unit cell of the slab]]
    """
    def __init__(self, slab, atom_numbers,
                 closest_allowed_distances, box_to_place_in=None):
        self.slab = slab
        self.atom_numbers = atom_numbers
        self.blmin = closest_allowed_distances
        if box_to_place_in is None:
            p0 = np.array([0., 0., 0.])
            cell = self.slab.get_cell()
            self.box = [p0, [cell[0, :], cell[1, :], cell[2, :]]]
        else:
            self.box = box_to_place_in

    def get_new_candidate(self):
        """ Returns a new candidate. """
        N = len(self.atom_numbers)
        cell = self.slab.get_cell()
        pbc = self.slab.get_pbc()

        # The ordering is shuffled so different atom
        # types are added in random order.
        order = list(range(N))
        shuffle(order)
        num = list(range(N))
        for i in range(N):
            num[i] = self.atom_numbers[order[i]]
        blmin = self.blmin

        # Runs until we have found a valid candidate.
        while True:
            pos = np.zeros((N, 3))
            # Make each new position one at a time.
            for i in range(N):
                pos_found = False
                pi = None
                while not pos_found:
                    pi = random_pos(self.box)
                    if i == 0:
                        break
                    isolated = True
                    too_close = False
                    for j in range(i):
                        d = get_mic_distance(pi, pos[j], cell, pbc)
                        bij_min = blmin[(num[i], num[j])]
                        bij_max = bij_min * 2.
                        if d < bij_min:
                            too_close = True
                            break
                        if d < bij_max:
                            isolated = False
                    # A new atom must be near something already there,
                    # but not too close.
                    if not isolated and not too_close:
                        pos_found = True
                pos[i] = pi

            # Put everything back in the original order.
            pos_ordered = np.zeros((N, 3))
            for i in range(N):
                pos_ordered[order[i]] = pos[i]
            pos = pos_ordered
            top = Atoms(self.atom_numbers, positions=pos, pbc=pbc, cell=cell)

            # At last it is verified that the new cluster is not too close
            # to the slab it is supported on.
            tf = False
            for i in range(len(self.slab)):
                for j in range(len(top)):
                    dmin = blmin[(self.slab.numbers[i], top.numbers[j])]
                    d = get_mic_distance(self.slab.positions[i],
                                         top.positions[j], cell, pbc)
                    if d < dmin:
                        tf = True
                        break
                if tf:
                    break
            if not tf:
                break
        return self.slab + top
