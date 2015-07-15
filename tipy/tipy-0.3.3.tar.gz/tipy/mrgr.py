#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Merger classes to merge results from several predictors."""

import tipy.prdct
from abc import ABCMeta, abstractmethod


class Merger(object):
    """Base class for all Mergers.

    G{classtree Merger}
    """

    __metaclass__ = ABCMeta
    MIN_PROBABILITY = 0.0
    MAX_PROBABILITY = 1.0

    def __init__(self):
        """Merger creator."""
        self.name = "Merger dosen't set any name"

    def filter(self, prediction):
        """Sort the tokens according to their probabilities.

        The duplicate tokens are merged to a single token (their probabilities
        are summed).

        @param prediction:
            It is a list of Suggestion instances.
        @type prediction: L{prdct.Prediction}

        @return:
            The sorted Prediction instance.
        @rtype: Prediction
        """
        seen_tokens = set()
        result = tipy.prdct.Prediction()
        for i, suggestion in enumerate(prediction):
            token = suggestion.word
            if token not in seen_tokens:
                for j in range(i + 1, len(prediction)):
                    if token == prediction[j].word:
                        suggestion.probability += prediction[j].probability
                        if suggestion.probability > self.MAX_PROBABILITY:
                            suggestion.probability = self.MAX_PROBABILITY
                        elif suggestion.probability < self.MIN_PROBABILITY:
                            suggestion.probability = self.MIN_PROBABILITY
                seen_tokens.add(token)
                result.add_suggestion(suggestion)
        return result

    @abstractmethod
    def merge(self, predictionList):
        """Method for merging predictors's prediction list.

        The merge() method is the main method of the Merger. It must be
        implemented by every Mergers.
        """
        raise NotImplementedError("Method must be implemented")


class ProbabilisticMerger(Merger):
    """Simple Merger which merge suggestions based on their probabilities.

    This Merger does not modify the suggestions probabilities. Thus, they are
    sorted in descending order according to their probabilities.

    G{classtree ProbabilisticMerger}
    """
    def __init__(self):
        """ProbabilisticMerger creator."""
        super(self.__class__, self).__init__()
        self.name = 'ProbabilisticMerger'

    def merge(self, predictionList):
        """merge the suggestions in a single list and sort them.

        @param predictionList:
            The list of Prediction instances. Each predictors return a
            Prediction instance which is added to the list by the
            PredictorActivator.
        @type predictionList: list

        @return:
            The merged Prediction instance containing every suggestions of
            every Prediction instances sorted in descending order according to
            their probabilities.
        @rtype: L{prdct.Prediction}
        """
        result = tipy.prdct.Prediction()
        for prediction in predictionList:
            for suggestion in prediction:
                result.add_suggestion(suggestion)
        return(self.filter(result))
