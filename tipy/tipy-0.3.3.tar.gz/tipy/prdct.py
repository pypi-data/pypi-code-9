#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Classes for predictors and to handle suggestions and predictions."""

from sys import exit
from tipy.db import SqliteDatabaseConnector
from tipy.mrgr import ProbabilisticMerger
from abc import ABCMeta, abstractmethod
from tipy.stpl import *
from math import exp
from multiprocessing import Queue, Process


class Suggestion(object):
    """A suggestion consists of a string and a probility.

    The string is in fact a token and the probability is the probability
    associated to this token by the predictor which compute it. The
    probability reflect how accurate the word is over prediction.

    G{classtree Suggestion}
    """

    def __init__(self, word, probability):
        """Suggestion creator

        A suggestion is a couple formed by a suggested word and its probability.

        @note: the probabilities of each predictors should have the same
            weight. Otherwise the suggestion selection will be truncated.

        @param word:
            The suggested word.
        @type word: str
        @param probability:
            The suggested word probability. It is compute by the predictors.
        @type probability: float
        """
        self.word = word
        self.probability = probability

    def __eq__(self, other):
        """Override the == operator in order to compare instances equality.

        Two Suggestion instances are equal if their word and probability are
        equal.

        @param other:
            The Suggestion instance to compare to this one (self).
        @type other: L{Suggestion}

        @return:
            True if the two instances are equal, False otherwise.
        @rtype:
            bool
        """
        if self.word == other.word and self.probability == other.probability:
            return True
        return False

    def __lt__(self, other):
        """Override the < operator in order to compare instances.

        A Suggestion instance is less than another if its probability is less
        than the probability of the other. If their probabilities are equal then
        the Suggestion instance is less than the other if its word is
        alphabetically 'before' the word of the other instance.

        @param other:
            The Suggestion instance to compare to this one (self).
        @type other: L{Suggestion}

        @return:
            True if the this instance (self) is less than the other one, False
            otherwise.
        @rtype: bool
        """
        if self.probability < other.probability:
            return True
        if self.probability == other.probability:
            return self.word < other.word
        return False

    def __gt__(self, other):
        """Override the > operator in order to compare instances.

        A Suggestion instance is greater than another if its probability is
        greater than the probability of the other. If their probabilities are
        equal then the Suggestion instance is greater than the other if its word
        is alphabetically 'after' the word of the other instance.

        @param other:
            The Suggestion instance to compare to this one (self).
        @type other: L{Suggestion}

        @return:
            True if the this instance (self) is greater than the other one,
            False otherwise.
        @rtype: bool
        """
        if self.probability > other.probability:
            return True
        if self.probability == other.probability:
            return self.word > other.word
        return False


class Prediction(list):
    """Class for predictions from predictors.

    A Prediction instance hold multiple Suggestion instances. It is a list of
    Suggestion instances and the list is kept ordered according to the
    suggestions probabilities.
    Every predictors should return a Preidiction instance.

    G{classtree Prediction}
    """

    def __init__(self):
        """Prediction creator."""
        pass

    def __eq__(self, other):
        """Override the == operator in order to compare instances.

        Two Prediction instances are equal if they contain the same items
        (thus, have the same length).
        """
        if self is other:
            return True
        if len(self) != len(other):
            return False
        for i, s in enumerate(other):
            if not s == self[i]:
                return False
        return True

    def add_suggestion(self, suggestion):
        """Add a suggestion in the Prediction list.

        The suggestion is added at the correct index so that the Prediction
        list remains ordered.

        @note: Using insert() and a while loop seams a little faster than using
               sorted(). Also, using insort from the bisect module seems to
               produce similar benchmarks.
        """
        if len(self) == 0:
            self.append(suggestion)
        else:
            i = 0
            while i < len(self) and suggestion < self[i]:
                i += 1
            self.insert(i, suggestion)


class PredictorActivator(object):
    """Query the predictors listed in the registry to get their suggestions.

    This class has access to a PredictorRegistry and asks the predictors listed
    in this PredictorRegistry to call their predict() method, store the
    resulting Prediction instances, merge them into a single Prediction
    instance and return it.

    G{classtree PredictorActivator}
    """

    def __init__(self, config, predictorRegistry):
        """PredictorActivator creator.

        @param config:
            The configuration dictionary is used in order to retrieve the
            PredictorActivator settings from the config file.
        @type config: L{drvr.Configuration}
        @param predictorRegistry:
            The class needs to access the PredictorRegistry to call their
            predict() method.
        @type predictorRegistry: L{PredictorRegistry}
        """
        self.config = config
        self.predictorRegistry = predictorRegistry
        self.predictionList = []
        self.maxPartialPredictionSize = self.config.getas(
            'PredictorActivator', 'max_partial_prediction_size', 'int') + 1
        self.mergingMethod = self.config.getas(
            'PredictorActivator', 'merging_method')
        self.stopListFile = self.config.getas(
            'PredictorActivator', 'stoplist')
        self.stopList = StopList(self.stopListFile)
        if self.mergingMethod.lower() == "probabilistic":
            self.merger = ProbabilisticMerger()
        else:
            lg.error('Unknown merging method')
            exit(1)

    def pred_worker(self, predictor, queue, factor):
        """Worker function for the predictor predict() methods.

        This method is used as the predictors workers target. It push the
        predictor's L{prdct.Predictor.predict} method result (a
        L{Prediction} instance) in a queue (which is used because it is
        thread-safe).

        @param predictor:
            The Predictor based class instance.
        @type predictor: L{Predictor} based class.
        @param queue:
            A queue in which the result will be pushed.
        @type queue:
            multiprocessing.Queue
        @param factor:
            A factor used to increase the number of suggestions.
        @type factor: int
        """
        queue.put(predictor.predict(
                  self.maxPartialPredictionSize * factor, self.stopList.words))

    def predict(self, factor=1):
        """Build a list of every predicted words.

        Call the predict() method of every predictors in the registry then
        merge their Prediction into a single Prediction instance.

        @change:
            - 16/06/15: The method now uses multi-processing. It concurrently
                runs every predictors's predict() method which allow a
                significant speed augmentation. The queue is used because it is
                thread safe. The point is that when the threads args are passed
                to the L{PredictorActivator.pred_worker()}, they are
                packed up with pickle, shipped to the other process, where they
                are unpacked used. A list wouldn't be passed but would be
                cloned.

        @note:
            Using multi-processing allow significant speed boost. The next
            benchmark have been maid runing 100 * 10 different contexts
            predictions::

            Total time without multi-processing: 86.785 s
            Total time wit multi-processing:     76.513 s

        @todo 0.0.9:
            Demonize the processes, set a timeout value. When the time runs out
            the unfinished workers return their results as is. This can alter
            the prediction qality but totaly avoid any possible "slow
            predictions".

        @param factor:
            A factor used to increase the number of suggestions.
        @type factor: int

        @return:
            The merged Prediction instance containing every suggestions of
            every Prediction instances sorted in descending order according to
            their probabilities.
        @rtype: L{Prediction}
        """
        self.predictionList[:] = []
        jobs = []
        queue = Queue()
        for predictor in self.predictorRegistry:
            p = Process(
                    target=self.pred_worker, args=(predictor, queue, factor,))
            jobs.append(p)
            p.start()
        for job in jobs:
            job.join()
        for x in range(len(jobs)):
            self.predictionList.append(queue.get())
        return self.merger.merge(self.predictionList)


class PredictorRegistry(list):
    """List every predictors instances that are to be used for word prediction.

    G{classtree PredictorRegistry}
    """

    def __init__(self, config):
        """PredictorRegistry creator.

        @param config:
            config is used to retrieve the PredictorRegistry settings and each
            Predictor settings from the config file. Also it needs to be passed
            to the predictors instances to allow them to retrieve their settings
            from the config file too.
        @type config: L{drvr.Configuration}
        """
        self._contextMonitor = None
        self.config = config
        self.contextMonitor = None

    def contextMonitor():

        def fget(self):
            return self._contextMonitor

        def fset(self, value):
            if self._contextMonitor is not value:
                self._contextMonitor = value
                self[:] = []
                self.set_predictors()

        def fdel(self):
            del self._contextMonitor

        return locals()
    contextMonitor = property(**contextMonitor())

    def set_predictors(self):
        """Read the configuration file and create needed predictors."""
        if self.contextMonitor:
            self[:] = []
            preds = self.config.getas('PredictorRegistry', 'predictors', 'list')
            for predictor in preds:
                self.add_predictor(predictor)

    def add_predictor(self, predictorName):
        """Create and add a predictor to the list.

        Create a predictor instance according to the predictor name and add
        it to the list.

        @param predictorName:
            The name of the predictor. It is used to retrieve the predictor
            settings from the config. It must correspond to a section of the
            config, otherwise no predictor will be created and added.
        @type predictorName: str
        """
        predictorClass = self.config.getas(predictorName, 'class')
        if predictorClass == 'WeightNgramPredictor':
            predictor = WeightNgramPredictor(
                self.config, self.contextMonitor, predictorName)
        elif predictorClass == 'LastOccurPredictor':
            predictor = LastOccurPredictor(
                self.config, self.contextMonitor, predictorName)
        elif predictorClass == 'MemorizePredictor':
            predictor = MemorizePredictor(
                self.config, self.contextMonitor, predictorName)
        elif predictorClass == 'DictionaryPredictor':
            predictor = DictionaryPredictor(
                self.config, self.contextMonitor, predictorName)
        else:
            predictor = None
        if predictor:
            self.append(predictor)

    def close_databases(self):
        """Close every opened predictors database."""
        for predictor in self:
            predictor.close_database()


class Predictor(object):
    """Base class for predictors.

    G{classtree Predictor}
    """

    __metaclass__ = ABCMeta

    def __init__(self, config, contextMonitor):
        """Predictor creator.

        @param config:
            The config is used to retrieve the predictor settings from the
            config file.
        @type config: L{Configuration}
        @param contextMonitor:
            The contextMonitor is needed because it allow the predictor to get
            the input buffers tokens.
        @type contextMonitor: L{ContextMonitor}
        """
        self.contextMonitor = contextMonitor
        self.name = "Predictor dosen't set any name"
        self.config = config

    @abstractmethod
    def predict(self, maxPartialPredictionSize, stopList):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def learn(self, text):
        raise NotImplementedError("Method must be implemented")


class WeightNgramPredictor(Predictor):
    """Compute prediction from n-gram model in database.

    G{classtree WeightNgramPredictor}
    """

    def __init__(self, config, contextMonitor, predictorName=None):
        """WeightNgramPredictor creator.

        @param config:
            The config is used to retrieve the predictor settings from the
            config file.
        @type config: L{drvr.Configuration}
        @param contextMonitor:
            The contextMonitor is needed because it allow the predictor to get
            the input buffers tokens.
        @type contextMonitor: L{ContextMonitor}
        @param predictorName:
            The custom name of the configuration using this predictor.
        @type predictorName: str
        """
        Predictor.__init__(self, config, contextMonitor)
        self.name = predictorName
        self.db = None
        self.dbFile = self.config.getas(self.name, 'database')
        self.deltas = self.config.getas(self.name, 'DELTAS', 'floatlist')
        self.learnMode = self.config.getas(self.name, 'learn', 'bool')
        self.maxN = len(self.deltas)
        self.init_database_connector()

    def init_database_connector(self):
        """Initialize the database connector.

        Using the database file path, the n-gram maximum size and the learn
        mode to initialize and open the database.
        """
        if self.dbFile and self.maxN > 0:
            self.db = SqliteDatabaseConnector(self.dbFile, self.maxN)

    def predict(self, maxPartialPredictionSize, stopList=[]):
        """Predict the next word according to the current context.

        Use the input buffers (thanks to contextMonitor) and the n-gram database
        to predict the most probable suggestions.
        A suggestion is a word which can:
            - Predict the end of the world. i.e. complete the actual partial
              word (the user has not finished to input the word, we try to
              predict the end of the word).
            - Predict the next word (the user has type a separator after a word,
              we try to predict the next word before he starts to type it).

        In order to compute the suggestions, this method:
            - Retrieve the last n tokens from the left input buffer ; where n is
              the maximum n-grams size (max(n)) which is stored in the database.
            - Loop for each n-gram size from max(n) to 1:
                - Find n-grams of current n-gram size in the database which
                  match the last input tokens.
                - Add each retrieved n-gram to the suggestion list if it is not
                  already in it and if we have not reach the maximum number of
                  suggestions yet.

        @param maxPartialPredictionSize:
            Maximum number of suggestion to compute. If this number is reached,
            the suggestions list is immediatly return.
            DatabaseConnector.ngram_table_tp() returns the records in descending
            order according to their number of occurences so the most probable
            suggestions will be added to the list first.
            This result in no suggestion quality loss, regardless of the desired
            number of suggestions.
        @type maxPartialPredictionSize: int
        @param stopList:
            The stoplist is a list of undesirable words. Any suggestion which
            is in the stopList won't be added to the suggestions list.
        @type stopList: list

        @return:
            A list of every suggestions possible (limited to
            maxPartialPredictionSize).
        @rtype: L{Prediction}
        """
        tokens = [''] * self.maxN
        for i in range(self.maxN):
            tokens[self.maxN - 1 - i] = self.contextMonitor.left_token(i)
        prefixCompletionCandidates = []
        for k in reversed(range(self.maxN)):
            if len(prefixCompletionCandidates) >= maxPartialPredictionSize:
                break
            prefixNgram = tokens[(len(tokens) - k - 1):]
            partial = None
            partial = self.db.ngram_table_tp(
                prefixNgram,
                maxPartialPredictionSize - len(prefixCompletionCandidates))
            for p in partial:
                if len(prefixCompletionCandidates) > maxPartialPredictionSize:
                    break
                candidate = p[-2]
                if candidate not in prefixCompletionCandidates:
                    if not candidate.lower() in stopList:
                        prefixCompletionCandidates.append(candidate)
        return self.weight(prefixCompletionCandidates, tokens)

    def weight(self, prefixCompletionCandidates, tokens):
        """Compute probability of suggestions and return the most probable ones.

        The probability of a suggestion is based on its relative frequency
        toward the whole set of suggestions and the number of single tokens in
        the database.

        @param prefixCompletionCandidates:
            List of every suggestions returned by self.predict().
        @type prefixCompletionCandidates: list
        @param tokens:
            The last input tokens.
        @type tokens: list

        @return:
            List of every "good enought" suggestions.
        @rtype: L{Prediction}
        """
        prediction = Prediction()
        unigramCountsSum = self.db.sum_ngrams_occ(1)
        for j, candidate in enumerate(prefixCompletionCandidates):
            tokens[self.maxN - 1] = candidate
            probability = 0
            for k in range(self.maxN):
                numerator = self.count(tokens, 0, k + 1)
                denominator = unigramCountsSum
                if numerator > 0:
                    denominator = self.count(tokens, -1, k)
                frequency = 0
                if denominator > 0:
                    frequency = float(numerator) / denominator
                probability += self.deltas[k] * frequency
            if probability > 0:
                prediction.add_suggestion(
                    Suggestion(tokens[self.maxN - 1], probability))
        return(prediction)

    def close_database(self):
        """Close the predictor's database."""
        self.close_database()

    def learn(self, change):
        """Learn what need to be learnt by adding n-grams in database.

        @param change:
            The part of the left input buffer which represent the last change.
        @type change: str
        """
        if self.learnMode is False:
            return
        ngramMap = self.make_ngram_map(change)
        ngramMap = self.prefix_ngrams_with_input(change, ngramMap)
        self.push_ngrams_in_db(ngramMap)

    def make_ngram_map(self, change):
        """Create a map associating n-grams (lists of words) and their count.

        @param change:
            The part of the left input buffer which represent the last change.
        @type change: str
        """
        ngramMap = {}
        for curCard in range(1, self.maxN + 1):
            changeIdx = 0
            changeSize = len(change)
            ngramList = ()
            for i in range(curCard - 1):
                if changeIdx >= changeSize:
                    break
                ngramList = ngramList + (change[changeIdx],)
                changeIdx += 1
            while changeIdx < changeSize:
                ngramList = ngramList + (change[changeIdx],)
                changeIdx += 1
                try:
                    ngramMap[ngramList] = ngramMap[ngramList] + 1
                except KeyError:
                    ngramMap[ngramList] = 1
                ngramList = ngramList[1:]
            curCard += 1
        return ngramMap

    def prefix_ngrams_with_input(self, change, ngramMap):
        """Use the input left buffer to expand the n-gram map.

        This method call L{cntxt.ContextMonitor.previous_tokens} to get the
        tokens from the left input buffer that are just before the change
        and add them BEFORE the change n-grams generated by
        L{self.make_ngram_map}.

        For instance, if the current left input buffer is::
            "phone is on the white table "

        And change is::
            "table"

        Then, the n-gram map generated by self.make_ngram_map() will be::
            {("table"): 1}

        The n-gram map contain a sinle n-gram of size 1. And so this method
        will add the tokens preceding the change in the left input buffer to
        form n-grams of size 2 and more (until it reaches self.maxN)::
            {("the", "white", "table"): 1, ("white", "table"): 1, {"table"): 1}

        @param change:
            The part of the left input buffer which represent the last change.
        @type change: str
        @param ngramMap:
            Dictionary associating n-grams with their number of occurences,
            generated by self.make_ngram_map().
        @type ngramMap: dict

        @return:
            The extanded n-grams dictionary.
        @rtype: dict
        """
        changeMatchInput = (change and
                            change[-1] == self.contextMonitor.left_token(1) and
                            self.contextMonitor.left_token(len(change)))
        if changeMatchInput:
            ngramList = tuple(change[:1])
            tkIdx = 1
            while len(ngramList) < self.maxN:
                extraToken = self.contextMonitor.previous_tokens(
                    tkIdx, change)
                if not extraToken:
                    break
                ngramList = (extraToken,) + ngramList
                try:
                    ngramMap[ngramList] = ngramMap[ngramList] + 1
                except KeyError:
                    ngramMap[ngramList] = 1
                tkIdx += 1
        return ngramMap

    def push_ngrams_in_db(self, ngramMap):
        """Update the database with the n-grams contained in the n-gram map.

        Each n-gram of the n-gram map is pushed into the database with its
        number of occurences (count).
        If the n-gram is already in the database then its count (number of
        occurences) is updated. If the n-gram is not in the database then it is
        simply inserted in it.

        @param ngramMap:
            Dictionary associating n-grams with their number of occurences,
            generated by L{self.make_ngram_map} and modified by
            L{self.prefix_ngrams_with_input}.
        @type ngramMap: dict
        """
        for ngram in ngramMap:
            count = self.db.ngram_count(ngram)
            if count > 0:
                self.db.update_ngram(ngram, count + ngramMap[ngram])
            else:
                self.db.insert_ngram(list(ngram), ngramMap[ngram])
        self.db.commit()

    def count(self, tokens, offset, n):
        """Make an n-gram then retrieve and return its 'count' entry in the db.

        @param tokens:
            The tokens used to make the n-gram.
        @type tokens: list
        @param offset:
            Offsset of the first token in the tokens.
        @type offset: int
        @param n:
            Size of the n-gram.
        @type n: int
        """
        if n > 0:
            ngram = tokens[len(tokens) - n + offset:len(tokens) + offset]
            result = self.db.ngram_count(ngram)
        else:
            result = self.db.sum_ngrams_occ(1)
        return result


class LastOccurPredictor(Predictor):
    """Compute predictions based on their last occurences and frequencies.

    G{classtree LastOccurPredictor}
    """

    def __init__(self, config, contextMonitor, predictorName=None):
        """LastOccurPredictor creator.

        @param config:
            The config is used to retrieve the predictor settings from the
            config file.
        @type config: L{drvr.Configuration}
        @param contextMonitor:
            The contextMonitor is needed because it allow the predictor to get
            the input buffers tokens.
        @type contextMonitor: L{ContextMonitor}
        @param predictorName:
            The custom name of the configuration using this predictor.
        @type predictorName: str
        """
        Predictor.__init__(self, config, contextMonitor)
        self.name = predictorName
        self.lambdav = self.config.getas(self.name, 'lambda', 'int')
        self.n0 = self.config.getas(self.name, 'n_0', 'int')
        self.cutoffThreshold = self.config.getas(
            self.name, 'cutoff_threshold', 'int')

    def predict(self, maxPartialPredictionSize, stopList=[]):
        """Compute the predictions using a simple exponential decay method.

        @param maxPartialPredictionSize:
            Maximum number of suggestion to compute. If this number is reached,
            the suggestions list is immediatly return.
            DatabaseConnector.ngram_table_tp() returns the records in descending
            order according to their number of occurences so the most probable
            suggestions will be added to the list first.
            This result in no suggestion quality loss, regardless of the desired
            number of suggestions.
        @type maxPartialPredictionSize: int
        @param stopList:
            The stoplist is a list of undesirable words. Any suggestion which
            is in the stopList won't be added to the suggestions list.
        @type stopList: list

        @return:
            A list of every suggestions possible (limited to
            maxPartialPredictionSize).
        @rtype: L{Prediction}
        """
        result = Prediction()
        prefix = self.contextMonitor.prefix()
        if prefix:
            index = 1
            token = self.contextMonitor.left_token(index)
            prob = 0
            while (token and
                   len(result) < maxPartialPredictionSize and
                   index <= self.cutoffThreshold):
                if token.startswith(prefix):
                    if not token.lower() in stopList:
                        prob = self.n0 * exp(- (self.lambdav * (index - 1)))
                        result.add_suggestion(Suggestion(token, prob))
                index += 1
                token = self.contextMonitor.left_token(index)
        return result

    def learn(self, text):
        """This predictor has no ability to learn."""
        pass


class MemorizePredictor(Predictor):
    """Predict words based on memorized (learnt) input tokens patterns.

    This predictor is capable of tokens memorization. It memorize the inputed
    tokens and try to predict the suggestion using memorized tokens and n-grams
    (group of consecutive tokens).

    G{classtree MemorizePredictor}
    """

    def __init__(self, config, contextMonitor, predictorName=None):
        """MemorizePredictor creator.

        @param config:
            The config is used to retrieve the predictor settings from the
            config file.
        @type config: L{drvr.Configuration}
        @param contextMonitor:
            The contextMonitor is needed because it allow the predictor to get
            the input buffers tokens.
        @type contextMonitor: L{ContextMonitor}
        @param predictorName:
            The custom name of the configuration using this predictor.
        @type predictorName: str
        """
        Predictor.__init__(self, config, contextMonitor)
        self.name = predictorName
        self.memory = self.config.getas(self.name, 'memory')
        self.trigger = self.config.getas(self.name, 'trigger', 'int')
        self.learnMode = self.config.getas(self.name, 'learn', 'bool')

    def predict(self, maxPartialPredictionSize, stopList):
        """Predict words based on memorized input tokens.

        @param maxPartialPredictionSize:
            Maximum number of suggestion to compute. If this number is reached,
            the suggestions list is immediatly return.
            DatabaseConnector.ngram_table_tp() returns the records in descending
            order according to their number of occurences so the most probable
            suggestions will be added to the list first.
            This result in no suggestion quality loss, regardless of the desired
            number of suggestions.
        @type maxPartialPredictionSize: int
        @param stopList:
            The stoplist is a list of undesirable words. Any suggestion which
            is in the stopList won't be added to the suggestions list.
        @type stopList: list

        @return:
            A list of every suggestions possible (limited to
            maxPartialPredictionSize).
        @rtype: L{Prediction}
        """
        result = Prediction()
        memTrigger = []
        try:
            memFile = open(self.memory, 'r+')
        except FileNotFoundError:
            lg_error('Cannot open file ' + self.memory)
            return
        if self.init_mem_trigg(memTrigger):
            rollingWindow = ''
            if self.init_rolling_window(rollingWindow, memFile):
                token = ''
                while memFile.write(token):
                    if memTrigger == rollingWindow:
                        if not token.lower() in stopList:
                            result.add_suggestion(Suggestion(token, 1.))
                    self.update_rolling_window(rollingWindow, token)
        memFile.close()
        return result

    def learn(self, change):
        """Learn what need to be learnt by tokens in the memory file.

        @param change:
            The part of the left input buffer which represent the last change.
        @type change: str
        """
        if self.learnMode is False:
            return
        try:
            memFile = open(self.memory, 'a')
        except FileNotFoundError:
            lg_error('Cannot open file ' + self.memory)
            return
        for tok in change:
            memFile.write(tok + '\n')
        memFile.close()

    def init_mem_trigg(self, memTrigger):
        result = False
        for i in range(self.trigger, 0, -1):
            memTrigger.append(self.contextMonitor.left_token(i))
        if not '' in memTrigger:
            result = True
        return result

    def init_rolling_window(self, rollingWindow, memFile):
        tmp = [x.strip('\n') for x in memFile.readlines()]
        token = ''
        count = 0
        while count < self.trigger and tmp[count]:
            count += 1
        return count == self.trigger

    def update_rolling_window(self, rollingWindow, token):
        rollingWindow = rollingWindow[1:]
        rollingWindow += token


class DictionaryPredictor(Predictor):
    """Very simple word predictor using a dictionary.

    The dictionary is a file containing one word per line. This predictor does
    not use n-grams and is therefore less effective than the predictors using
    n-grams because it does not consider context.

    G{classtree DictionaryPredictor}
    """

    def __init__(self, config, contextMonitor, predictorName):
        """DictionaryPredictor creator.

        @note: The string.lower() and string.strip() methods have a great impact
            on performance (the profile module show that they require almost
            1 second of processing time when calculating suggestions for 10
            contexts. So this constructor no more directly use the dictionary
            file. A database is created instead.
            Every words of the dictionary are lowered and stripped then added
            to the database.
            Doing so, the performance of the predictor are way better.
            Profiling a script querying suggestions for 10 successive contexts
            show the improvement profits:
                - lower()ing and strip()ping each word of the file on each
                  predict() call::
                      ncalls  tottime  percall  cumtime  percall filename:lineno
                      690048    0.468    0.000    0.468    0.000 :0(lower)
                - Creating an improved list upon initialization and using it on
                  each predict() call (previous optimization method)::
                      ncalls  tottime  percall  cumtime  percall filename:lineno
                      100046    0.059    0.000    0.059    0.000 :0(lower)
                  It is approx. 800% faster. But this profiling mix
                  initialization and later computation. It means than most of
                  the time of the previous profiling line is spend in
                  initializing the list, computation on each predict() call are
                  even more profitable.
                - Creating a database and querying it on each predict() call::
                      ncalls  tottime  percall  cumtime  percall filename:lineno
                      100046    0.059    0.000    0.059    0.000 :0(lower)
                  It is not faster than the previous method but the database
                  must only be created once. And once it is created the
                  initialization time is (near) null and the querying time on
                  each predict() call is even faster.

        @change:
            - 08/06/15: Method now create an ordered optimized list containing
                dictionary words upon initialization in order to increase the
                speed of the predictor.
            - 13/06/15: Method now use a database containing the dictionary
                words. See: L{minr.DictMiner}

        @param config:
            The config is used to retrieve the predictor settings from the
            config file.
        @type config: L{drvr.Configuration}
        @param contextMonitor:
            The contextMonitor is needed because it allow the predictor to get
            the input buffers tokens.
        @type contextMonitor: L{ContextMonitor}
        @param predictorName:
            The custom name of the configuration using this predictor.
        @type predictorName: str
        """
        Predictor.__init__(self, config, contextMonitor)
        self.name = predictorName
        self.dbFile = self.config.getas(self.name, 'database')
        self.db = None
        self.prob = self.config.getas(self.name, 'probability', 'float')
        self.init_database_connector()

    def init_database_connector(self):
        """Initialize the database connector.

        Using the database file path, the n-gram maximum size and the learn
        mode to initialize and open the database.
        """
        if self.dbFile:
            self.db = SqliteDatabaseConnector(self.dbFile)

    def get_dict_range(self, prefix):
        """Select the dictionary range where words starts with the given prefix.

        A suggested word must complete the given token, it means that suggested
        words all start with this token, here called the prefix.
        This method create a list containing the suggested words for the
        given prefix, i.e. every words of the dictionary list starting with
        the prefix.
        It is easy as the dictionary list is ordered. For instance:

        If the prefix is::
            'hell'

        And the dictionary list is::
            ['bird', 'blue', 'given', 'hair', 'hellish', 'hello', 'red', 'zip']

        We first remove every words of the list one by one until we reach a word
        which actualy starts with the prefix 'hell', then we have::
            ['hellish', 'hello', 'red', 'zip']

        Finaly we scan every words of the remaining list and when we reach a
        word which does not starts with the given prefix then we know that every
        remaining words won't start with the prefix neither as the list is
        ordered, so we have::
            ['hellish', 'hello']

        @deprecated: This method has become useless since the words are now
                     stored in a database.

        @param prefix:
            The prefix from which suggested words range is computed.
        @type prefix: str
        """
        rangeWords = []
        for word in self.dictWords:
            if word.startswith(prefix):
                rangeWords = self.dictWords[self.dictWords.index(word):]
                break
        for word in rangeWords:
            if not word.startswith(prefix):
                rangeWords = rangeWords[:rangeWords.index(word)]
                break
        return rangeWords

    def predict(self, maxPartialPredictionSize, stopList):
        """Complete the actual word or predict the next word using dictionary.

        Use the input buffers (thanks to contextMonitor) and the word dictionary
        to predict the most probable suggestions.
        A suggestion is a word which can:
            - Predict the end of the world. i.e. complete the actual partial
              word (the user has not finished to input the word, we try to
              predict the end of the word).
            - Predict the next word (the user has type a separator after a
              word, we try to predict the next word before he starts to type
              it).

        In order to compute the suggestions, this method:
            - Retrieve the last token from the left input buffer.
            - Loop for each word in the dictionary:
                - If the word starts with the last token retrieved: add it to
                  the suggestion list if we have not reach the maximum number of
                  suggestions yet.
                  It is not necessary to check if the word is already in the
                  suggestion list because in a dictionary a word should only
                  appear once. In any case, the merger will merge the
                  duplicate suggestions.

        @param maxPartialPredictionSize:
            Maximum number of suggestion to compute. If this number is reached,
            the suggestions list is immediatly return.
            DatabaseConnector.ngram_table_tp() returns the records in descending
            order according to their number of occurences so the most probable
            suggestions will be added to the list first.
            This result in no suggestion quality loss, regardless of the desired
            number of suggestions.
        @type maxPartialPredictionSize: int
        @param stopList:
            The stoplist is a list of undesirable words. Any suggestion which
            is in the stopList won't be added to the suggestions list.
        @type stopList: list

        @return:
            A list of every suggestions possible (limited to
            maxPartialPredictionSize).
        @rtype: L{Prediction}
        """
        result = Prediction()
        prefix = self.contextMonitor.prefix().lower()
        count = 0
        candidates = self.db.ngram_table_tp([prefix], maxPartialPredictionSize)
        for candidate in candidates:
            if count > maxPartialPredictionSize:
                break
            candidate = candidate[-2]
            if not candidate in stopList:
                result.add_suggestion(Suggestion(candidate, self.prob))
                count += 1
        return result

    def learn(self, text):
        """This predictor has no ability to learn."""
        pass
