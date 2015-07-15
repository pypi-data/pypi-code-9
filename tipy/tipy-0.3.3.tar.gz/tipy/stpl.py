#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Stoplist class holds a list of (undesired) words."""


class StopList(object):
    """Stoplist classes holding every words of the stoplist(s).

    The program's predictors test every suggested words against the stoplist. If
    a suggested word is a stoplist word then the suggested word is not added to
    the suggested words list.

    G{classtree StopList}
    """

    def __init__(self, stopListFile):
        """Extract every words of the file and store them in a list.

        The file must contains one word per line. The method dosen't lower any
        word.

        @param stopListFile:
            Path to the stoplist file.
        @type stopListFile: str
        """
        self.stopListFile = stopListFile
        self.words = []
        if self.stopListFile:
            try:
                with open(self.stopListFile) as f:
                    self.words = [x.strip('\n') for x in f.readlines()]
            except IOError:
                lg.error('Cannot open file "%s". Stop list won\'t be used'
                         % (self.stopListFile))
        self.size = len(self.words)

    def add_words(self, wordList):
        """Add words to the stoplist.

        @param wordList:
            The words to add.
        @type wordList: list
        """
        for word in wordList:
            self.add_word(word)

    def add_word(self, word):
        """Add a word to the stoplist.

        @param word:
            The word to add.
        @type word: str
        """
        self.words.append(word)
        self.size += 1

    def remove_words(self, wordList):
        """Remove words from the stoplist.

        @param wordList:
            The words to remove.
        @type wordList: list
        """
        for word in wordList:
            self.remove_word(word)

    def remove_word(self, word):
        """Remove a word from the stoplist.

        @param word:
            The word to remove.
        @type word: str
        """
        try:
            self.words.remove(word)
            self.size -= 1
        except ValueError:
            print('WARNING: "' + word + '" is not in stop list')
