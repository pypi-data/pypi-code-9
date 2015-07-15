#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Classes for context monitoring and context change detection.

The context is determined by the input buffers contained in the Callback class.
It is necessary to monitor the context in order to know what the user is typing
and compute accurate predictive suggestions.
"""

from tipy.char import blankspaces, separators, is_word_char, last_word_char
from tipy.tknz import ReverseTokenizer, ForwardTokenizer
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ContextChangeDetector(object):
    """Detect context change.

    A context change can occure when some special characters appear in the
    buffers:
        - Word characters indicate that the current token is a (partial) word.
        - Blankspaces indicate the separations between two words. They mark
          the end of the current token.
        - Separators indicate a separation between two words. The dot separator
          mark the end of the sentence (and of the token) so the next token and
          suggestions should begin with an uppercase letter.
        - Special characters are non-printable characters such as backspace and
          arrow keys which are used to modify the input buffers.

    It is important to detect context change because some operations such as
    n-gram learning from input or suggested words suppression have to be carried
    out upon context changes.

    G{classtree ContextChangeDetector}
    """

    def __init__(self, lowercase, config):
        """ContextChangeDetector creator.

        @param config:
            It is used to retrieve the ContextMonitor settings from the
            configuration file.
        @type config: L{drvr.Configuration}
        @param lowercase:
            Indicate if the tokens should be convert to lowercase.
        @type lowercase: boolean
        """
        self.lowercase = lowercase
        self.config = config
        self.monitoredScopeSize = self.config.getas(
            'ContextMonitor', 'monitored_scope', 'int')
        self.monitoredScope = ''

    def update_monitored_scope(self, string):
        """Move the monitored scope according to the string length.

        @param string:
            Every characters inputed in the monitored buffer.
        @type string: str
        """
        if len(string) <= self.monitoredScopeSize:
            self.monitoredScope = string
        else:
            self.monitoredScope = string[:-self.monitoredScopeSize]

    def context_change(self, leftBuffer):
        """Check if the context has changed.

        To determine if a context change occure or not it is important to
        scan the input left buffer and the monitored scope. A change occure if:
            - The monitored scope is not part of the left buffer.
            - The monitored scope is part of the left buffer and a separator
              character appear in the left buffer part wich is not the monitored
              scope.

        @param leftBuffer:
            The input left buffer.
        @type leftBuffer: str

        @return:
            True or False weither the context has changed or not.
        @rtype: boolean
        """
        prevContext = self.monitoredScope
        currContext = leftBuffer
        if len(prevContext) == 0:
            if len(currContext) == 0:
                return False
            else:
                return True
        iIdx = currContext.rfind(prevContext)
        if iIdx == -1:
            return True
        rest = currContext[iIdx + len(prevContext):]
        idx = last_word_char(rest)
        if idx == -1:
            if len(rest) == 0:
                return False
            last_char = currContext[iIdx + len(prevContext) - 1]
            if is_word_char(last_char):
                return True
            else:
                return False
        if idx == len(rest) - 1:
            return False
        return True

    def change(self, leftBuffer):
        """Return the (part of the) token(s) appearing after a change.

        When a change occure it is necessary to retrieve the characters forming
        (partial) tokens which have been inputed AFTER the change and this is
        what this method do.
        Weither a change occure or not is determined by self.context_change().

        @note: If no change have been registered yet then the leftBuffer is
               returned.

        @param leftBuffer:
            The input left buffer.
        @type leftBuffer: str

        @return:
            (Part of) tokens inputed after the last change.
        @rtype: list
        """
        prevContext = self.monitoredScope
        currContext = leftBuffer
        if len(prevContext) == 0:
            return currContext
        iIdx = currContext.rfind(prevContext)
        if iIdx == -1:
            return currContext
        result = currContext[iIdx + len(prevContext):]
        if self.context_change(leftBuffer):
            tokenizer = ReverseTokenizer(prevContext, self.lowercase)
            firstToken = tokenizer.next_token()
            if not len(firstToken) == 0:
                result = firstToken + result
        return result


class ContextMonitor(object):   # observer.Observer
    """Monitire user current context.

    This class monitore the input buffers in order to:
        - Tokenize the input and use the tokens for prediction.
        - Identify context changes.

    G{classtree ContextMonitor}
    """

    def __init__(self, config, predictorRegistry, callback):
        """ContextMonitor creator.

        @param config:
            It is used to retrieve the ContextMonitor settings from the
            configuration file.
        @type config: L{drvr.Configuration}
        @param predictorRegistry:
            It is used to access the predictors's learn() methods. Also, the
            ContextMonitor is used by the predictors to access the input
            buffers.
        @type predictorRegistry: L{PredictorRegistry}
        @param callback:
            As the callback hold the input buffers and the ContextMonitor
            operate on these buffers, it is used to access the input buffers
            from inside the ContextMonitor.
        @type callback: L{Callback}
        """
        self.config = config
        self.lowercase = self.config.getas(
            'ContextMonitor', 'lowercase', 'bool')
        self.liveLearning = self.config.getas(
            'ContextMonitor', 'live_learning', 'bool')
        self.predictorRegistry = predictorRegistry
        self.callback = callback
        self.contextChangeDetector = ContextChangeDetector(
            self.lowercase, self.config)
        self.predictorRegistry.contextMonitor = self

    def context_change(self):
        """Check if a context change occure.

        @return:
            Return True or False weither a context change occure.
        @rtype: bool
        """
        return self.contextChangeDetector.context_change(self.left_buffer())

    def update(self):
        """Check if context changes occure and learn what need to be learnt.

        This method is called by Driver.predict() after the predictions have
        been computed. It check if a context change occure in the input
        buffers and if so, it learn the words that need to be learnt if the
        predictor's learning mode is ON. Finaly, it update the monitored scope.
        """
        change = self.contextChangeDetector.change(self.left_buffer())
        if self.liveLearning and change:
            self.learn(change)
        self.contextChangeDetector.update_monitored_scope(self.left_buffer())

    def learn(self, string):
        """Learn n-grams from the input buffers.

        Trigger the learn() method of each predictor of the registry. This
        method use the input buffers to create n-grams and add them to the
        predictors's databases or memory so that the program learn from the
        user input.

        @param string:
            The string to learn.
        @type string: str
        """
        tokens = []
        tok = ForwardTokenizer(string, self.lowercase, blankspaces, separators)
        while tok.has_more_tokens():
            token = tok.next_token()
            tokens.append(token)
        if tokens:
            tokens = tokens[:-1]
        for predictor in self.predictorRegistry:
            predictor.learn(tokens)

    def prefix(self):
        """Return the token just before the cursor.

        @return:
            The token just before the cursor or an empty string if there is
            none.
        @rtype: str
        """
        return self.left_token(0)

    def suffix(self):
        """Return the token just after the cursor.

        @return:
            The token just after the cursor or the empty string if there is
            none.
        @rtype: str
        """
        return self.right_token(0)

    def left_token(self, index):
        """Return the token at a given index in the left input buffer.

        @param index:
            The index of the token to retrieve in the left input buffer.
        @type index: int

        @return:
            The token at index 'index' in the left input buffer or an empty
            string if the token dosen't exists.
        @rtype: str
        """
        leftInput = self.left_buffer()
        tok = ReverseTokenizer(leftInput, self.lowercase)
        i = 0
        while tok.has_more_tokens() and i <= index:
            token = tok.next_token()
            i += 1
        if i <= index:
            token = ''
        return token

    def right_token(self, index):
        """Return the token at a given index in the right input buffer.

        @param index:
            The index of the token to retrieve in the right input buffer.
        @type index: int

        @return:
            The token at index 'index' in the right input buffer or an empty
            string if the token dosen't exists.
        @rtype: str
        """
        tok = ForwardTokenizer(self.right, self.lowercase)
        i = 0
        while tok.has_more_tokens() and i <= index:
            token = tok.next_token()
            i += 1
        if i <= index:
            token = ''
        return token

    def previous_tokens(self, index, change):
        """Return the token just before the change token (if any).

        This method is called in some predictors's learn() method. It retrieve
        the token that appear just before the change token and has already
        been learnt before (or should have). The previous token is used to fill
        the n-grams.

        @param index:
            Index of the previous token.
        @type index: int
        @param change:
            The change token.
        @type change: str

        @return:
            The token just before the change token or an empty string if there
            is none.
        @rtype: str
        """
        return self.left_token(index + len(change))

    def left_buffer(self):
        """Use the callback to get the value of the left buffer.

        @return:
            The left input buffer.
        @rtype: str
        """
        return self.callback.left

    def right_buffer(self):
        """Use the callback to get the value of the right buffer.

        @return:
            The right input buffer.
        @rtype:
            str
        """
        return self.callback.right

    def make_completion(self, suggestion):
        """Compute the completion string given a suggested word.

        This method compute and return the completion string using the token
        just before the cursor (prefix) and the suggested word (suggestion).
        The suggestion should be the word that the user choose from the
        suggested words list.

        For instance, if the prefix is::
            "wor"
        And the suggestion is::
            "world"
        Then this method will compute the completion::
            "ld"

        If the character before the cursor is a blankspace or a separator then
        the prefix should be empty::
            ""
        Then if the suggestion is::
            "guilty"
        This method will compute the completion::
            "guilty"

        If the suggestion and the prefix don't match then False is returned.
        This should never happen as suggestions completing an input word should
        always match it. Still, I prefer to check it at the cost of some lower()
        and startswith() calls.

        @param suggestion:
            The suggested word from which to compute the completion.
        @type suggestion: str
        """
        prefix = self.prefix()
        if suggestion.lower().startswith(prefix.lower()):
            return suggestion[len(prefix):]
        return False
