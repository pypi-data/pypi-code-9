"""search type utilities"""
# https://gist.github.com/kirbyfan64/5fad06f7a70e6420bb8c
# http://blog.amjith.com/fuzzyfinder-in-10-lines-of-python

# std py3k stanza
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def fuzzy_distance(srch, straw):
    '''calculate distance between search and straw from haystack
    a distance of 0 indicates a search failure on one or more chars in srch.
    the lower the distance the closer the match, matching earlier and closer
    together creates a shorter distance.'''
    # finding complete srch term together is closer than seperated
    try:
        return straw.lower().index(srch.lower()) + 1
    except ValueError:
        pass

    last_match = 0
    distance = len(straw)  # penalty for not being adjoining
    for char in srch:
        try:
            last_match += straw[last_match:].lower().index(char.lower())
            distance += last_match
        except ValueError:
            return 0
    return distance


def fuzzy_search(needle, haystack):
    '''return those elements from haystack, ranked by distance from needle'''
    # decorate
    intermediate = []
    for straw in haystack:
        distance = fuzzy_distance(needle, straw)
        if distance:
            intermediate.append((distance, straw))
    # sort by distance
    intermediate.sort(key=lambda x: x[0])
    # undecorate and return
    return [x[1] for x in intermediate]
