#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Combiner classes to merge results from several predictors."""

import tipy.prdct
import abc


class Combiner(object):
    """Base class for all combiners.

    G{classtree Combiner}
    """

    __metaclass__ = abc.ABCMeta
    MIN_PROBABILITY = 0.0
    MAX_PROBABILITY = 1.0

    def __init__(self):
        """Combiner creator."""
        self.name = "Combiner dosen't set any name"

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

    @abc.abstractmethod
    def combine(self, predictionList):
        """Method for combining predictors's prediction list.

        The combine() method is the main method of the Combiner. It must be
        implemented by every combiners.
        """
        raise NotImplementedError("Method must be implemented")


class ProbabilisticCombiner(Combiner):
    """Simple combiner which combine suggestions based on their probabilities.

    This combiner does not modify the suggestions probabilities. Thus, they are
    sorted in descending order according to their probabilities.

    G{classtree ProbabilisticCombiner}
    """
    def __init__(self):
        """ProbabilisticCombiner creator."""
        super(self.__class__, self).__init__()
        self.name = 'ProbabilisticCombiner'

    def combine(self, predictionList):
        """Combine the suggestions in a single list and sort them.

        @param predictionList:
            The list of Prediction instances. Each predictors return a
            Prediction instance which is added to the list by the
            PredictorActivator.
        @type predictionList: list

        @return:
            The combined Prediction instance containing every suggestions of
            every Prediction instances sorted in descending order according to
            their probabilities.
        @rtype: L{prdct.Prediction}
        """
        result = tipy.prdct.Prediction()
        for prediction in predictionList:
            for suggestion in prediction:
                result.add_suggestion(suggestion)
        return(self.filter(result))
