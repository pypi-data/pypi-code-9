# -*- coding: utf-8 -*-
from collections import OrderedDict
from json import dump, dumps
import csv


class StateNeighbors(object):
    """
    Object that handles the finding of nieghbors

    :param file_name: CSV that contains pairings of states
    :param ordered: Whether or not to use an `OrderedDict` so that the states
        are all in order. If set to `False`, then a normal `dict` will be used.
    :param contiguous: How to handle stats that have no boardering states (ie.
        Alaska and Hawaii) If set to `True` then states without neighbors will
        not have any neighbors. If `False` then the nearest state to a non-
        contiguous state will be considerd its neighbor.
    :param allow_blank: Only used if `contiguous==True`. If this is set to
        `True`, then states that have no neighbors will return an empty list.
        If it is `False`, then states with no neighbors will be removed from
        the dictionary. This will raise a `ValueError` if a non-contiguous
        state is suplied as an argument.

    """
    def __init__(self, file_name='state_neighbors/state_neighbors.csv', ordered=True,
                 contiguous=False, allow_blank=False):
        self.file_name = file_name
        self.ordered = ordered
        self.contiguous = contiguous
        self.allow_blank = allow_blank
        self.states = self.get_state_neighbors_dict()

    def get_state_neighbors_dict(self):
        """
        Loads the cvs and parses the file to create an `OrderedDict` if
        ordered is set to `True`, else it will return a `dict`. This also
        handles states that are not contiguous and either removes them
        (`contiguous=True`) and allows for empty lists to be returned.
        """
        with open('state_neighbors.csv') as csvfile:
            states = OrderedDict() if self.ordered else dict()
            reader = csv.DictReader(csvfile)
            for row in reader:
                states.setdefault(row['state'], []).append(row['neighbor'])
            if self.contiguous:
                states.popitem('AK')
                states.popitem('HI')
                if self.allow_blank:
                    states.update({'AK', []})
                    states.update({'HI', []})
        return states

    def state_neighbors(self, state):
        """
        Creates the list of neighbors from `neighbors` for a the given `state`.
        This is the function that will most likey be used. As such the global
        `neighboring` funtion is set to this funtion from an initialized obj.

        :pram state: A state the is in `file_name` and now in `states`

        :returns: An list of states that neighbor `state`.
        :rtype: list
        """
        neighbors = []
        try:
            for neighbor in self.states[state]:
                neighbors.append(neighbor)
        except KeyError:
            raise ValueError("Could not find the state \"%s\"" % state)
        return neighbors

    def neighbors(self, depth=1):
        """
        Creates the nested dictonary that holds the states and thier neighbors
        in a list.

        :pram depth: How far to follow neighbors, as in a `depth=2` would
            produce a list of dictonarys with keys being the state and then the
            neighbors of that state as a list. Used to get states that are not
            neighbors of a state, but that states neighbors as well. Not
            Implemented currently.

        :returns: An `OrderedDict` or `dict` of states as keys, with the value
            as the list of states that are neighbors to it.
        :rtype: OrderedDict, dict

        .. todo: Allow for a depth that is greater than one.
        """
        if depth != 1:
            raise NotImplementedError
        neighbors = OrderedDict() if self.ordered else dict()
        states = self.states.keys()
        for _ in range(depth):
            for state in states:
                state_neighbor = self.state_neighbors(state)
                neighbors.setdefault(state, []).append(state_neighbor)
        return neighbors

    def json(self, depth=1, file_name=None):
        """
        Produces the dictionary of states as a json string, or outputs the json
        to file.

        :pram depth: Passed directly to `neighbors()`
        :pram file_name: If `file_name` is provided, the json will output to
            that file and return `True`.

        :rtype: bool, str

        .. seealso: neighbors()
        """
        if file_name:
            with open(file_name, 'w') as output:
                dump(self.neighbors(depth), output)
            return True
        else:
            return dumps(self.neighbors(depth))


_state_neighbors = StateNeighbors()
neighboring = _state_neighbors.state_neighbors
STATES = _state_neighbors.states
