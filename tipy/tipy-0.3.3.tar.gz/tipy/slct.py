#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Selector select suggested words in the list depending on various criteria.
"""

from collections import OrderedDict


class Selector(object):
    """The Selector class select the best suggested words among all.

    The goal of the selector is to clean the suggested words list (contained in
    a Prediction instance which should have been returned by a
    L{Merger<mrgr>} L{merge()<mrgr.Merger.merge>} method and remove
    the words which are too much (the configuration specify the excpected number
    of suggested  words).

    G{classtree Selector}
    """

    def __init__(self, config, contextMonitor):
        """Selector creator.

        @param config:
            The configuration dictionary is used in order to retrieve the
            Selector settings from the config file.
        @type config: L{drvr.Configuration}
        @param contextMonitor:
            The ContextMonitor is used to check if a context change occure. In
            which case the suggested words list must be cleared because
            prediction fully depends on the context.
        @type contextMonitor: L{ContextMonitor}
        """
        self.contextMonitor = contextMonitor
        self.config = config
        self.suggestions = self.config.getas('Selector', 'suggestions', 'int')
        self.suggestedWords = []

    def select(self, prediction):
        """Select suggested words in the suggestions list.

        Selecting suggested words consists in:
            - List every suggestions words.
            - Remove duplicate suggested words.
            - Shorten the suggested words list so that it contains the desired
              number og suggested words.

        @param prediction:
            The list of suggestions from which to carry out the selection.
        @type prediction: L{Prediction}
        """
        words = [sugg.word for sugg in prediction]
        if self.contextMonitor.context_change():
            self.suggestedWords = []
        self.rm_duplicate(words)
        if len(words) > self.suggestions:
            words = words[:self.suggestions]
        self.suggestedWords += words
        return words

    def rm_duplicate(self, words):
        """Remove duplicate words in the list and keep the original order.

        @param words:
            The words to filter.
        @type words: list
        """
        self.suggestedWords = list(
            OrderedDict.fromkeys(self.suggestedWords + words))
