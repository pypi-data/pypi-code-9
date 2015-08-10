# coding: utf-8
"""A library for item-to-item collaborative filtering.

The primary function of interest is `calculate_similarity`, which will
calculate similarity scores for pairs of items from a given dataset.

There are also a few similarity calculations to choose from in the `similarity`
module.

This library is in an extremely early state.

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import itertools


def get_dict_values(item_a, item_b, data):
    """Get index-aligned lists for all values in item_a and item_b.

    >>> # This is a slightly strange example since the order of the keys is
    >>> # arbitrary. The order doesn't matter, however the pairing does, which
    >>> # is why a set() of the zip() of the two lists should show the function
    >>> # is correct.
    >>>
    >>> one_items, two_items = get_dict_values('one', 'two',
    ...     {'one': {'a': 9, 'b': 50},
    ...      'two': {'a': 7, 'b': 35},
    ...      'three': {'a': 9999}})
    >>> set(zip(one_items, two_items)) == {(9, 7), (50, 35)}
    True

    """
    data_a = data[item_a]
    data_b = data[item_b]
    all_keys = set(data_a.keys()) | set(data_b.keys())
    a_values = [data_a.get(k, 0) for k in all_keys]
    b_values = [data_b.get(k, 0) for k in all_keys]
    return a_values, b_values


def calculate_similarity(dataset, similarity, result_storage=None,
                         get_values=get_dict_values):
    """Get a map of items to similar items using a ranking dataset.

    result_storage:
        an object implementing __getitem__ where all results are stored.

    get_values:
        a callable taking two keys and the dataset, which needs to return two
        lists, essentially 'vectorizing' the data from the dataset for the two
        items. See get_dict_values() for an example.

    """
    result = result_storage if result_storage is not None else {}
    for item_a, item_b in itertools.combinations(dataset, 2):
        a_values, b_values = get_values(item_a, item_b, dataset)
        sim_score = similarity(a_values, b_values)
        result[(item_a, item_b)] = sim_score
    return result


# TODO: functions below are untested; I do not need these functions myself yet
# so they sit here as untested prototypes
def __similar_sets(dataset, target, similarity):  # pragma: no cover
    """Find other entries most similar to target.

    dataset is a dict of score mappings.

    target is the key in dataset of the thing that the other things should be
    similar to.

    """
    target_data = dataset[target]
    scores = ((similarity(target_data, dataset[k]), k)
              for k in dataset if k != target)
    return sorted(scores, reverse=True)


def __recommend(similar_data, target):  # pragma: no cover
    """Recommend things to `target` using prebuilt similarity data.

    Target should be a user profile (e.g. a scores map), not a user's name.

    """
    scores = {}
    for item, rating in target.items():
        for similarity, other_item in similar_data[item]:

            # target has rated this item so don't recommend it
            if target.get(other_item, 0) != 0:
                continue
            scores.setdefault(other_item, 0)
            scores[other_item] += similarity * rating

    rankings = ((score, item) for item, score in scores.items())
    return sorted(rankings, reverse=True)
