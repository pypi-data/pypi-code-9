#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Driver class holds everything the program needs to perform prediction.

It gather instances of needed classes, implement some wrapper methods and the
very important L{drvr.Driver.predict} method which actualy compute the suggested
words.
"""

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from tipy.clbk import Callback
from tipy.slct import Selector
from tipy.prdct import PredictorRegistry, PredictorActivator
from tipy.cntxt import ContextMonitor
from os import path
from tipy.lg import lg


class UnknownTypeCastError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Unknown cast type "%s"' % self.value)


class MissingConfigurationSection(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Section "%s" is missing from the configuration'
                    % self.value)


class MissingConfigurationOption(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Section "%s" is missing from the configuration'
                    % self.value)


class Configuration(ConfigParser):
    """Copy a configuration file (ini format) in memory.

    This class subclass the Configparser class. Configparser is used to read() a
    configuration file (ini format) in memory in the form of a dictionary
    associating sections and options.
    This class implement a new method which allow to retrieve and cast a
    configuration option and asserts the option do exists and can be casted.
    The config file could be edited by the user and you know... never trust
    user input.

    G{classtree Configuration}
    """

    def __init__(self):
        """Configuration creator."""
        super().__init__()

    def getas(self, section, option, typeCast=None):
        """A more secure way to retrieve configuration options.

        This method check if the section and the option is in the configuration
        dictionary, else it raise an error. Also this method allow an optional
        parameter for casting the result before returning it. Allowed type
        casting are:
            - bool: cast to bool
            - int: cas to int
            - float: cast to float
            - list: cast to list
            - intlist: cast to list and cast each element to int
            - floatlist: cast to list and cast each element to float
        The method makes sure the casting is possible.

        @param section:
            The section from which to retrieve the option.
        @type section: str
        @param option:
            The option to retrieve inside the section.
        @type option: str
        @param typeCast:
            Indicate how to cast the result. If no value are passed the
            result is returned as a string.

        @return:
            The casted value of the given option found inside the given section.
        @rtype:
            str or int or bool or float or list (depends on "typeCast" param)

        @raise MissingConfigurationSection:
            If the given section cannot be found in the configuration
            dictionary.
        @raise MissingConfigurationOption:
            If the given option cannot be found in the configuration dictionary.
        @raise UnknownTypeCastError:
            If the given typeCast value is not "bool", "int", "float", "list",
            "intlist" or "floatlist".
        """
        if not self.has_section(section):
            raise MissingConfigurationSection(section)
        if not self.has_option(section, option):
            raise MissingConfigurationOption(option)
        if not typeCast or typeCast == 'str':
            return self.get(section, option)
        if typeCast == 'bool':
            return self.getboolean(section, option)
        if typeCast == 'int':
            return self.getint(section, option)
        if typeCast == 'float':
            return self.getfloat(section, option)
        if typeCast == 'list':
            return self.get(section, option).split()
        if typeCast == 'intlist':
            return [int(x) for x in self.get(section, option).split()]
        if typeCast == 'floatlist':
            return [float(x) for x in self.get(section, option).split()]
        raise UnknownTypeCastError(typeCast)


class Driver:
    """The Driver class gather classes inctances and variables of the program.

    G{classtree Driver}
    """

    def __init__(self, callback, configFile=''):
        """The driver class. It hold every elements needed for the prediction.

        @param callback:
            The callback is used to access the input buffers from anywhere.
        @type callback: L{Callback}
        @param configFile:
            Path of the configuration file.
        @type configFile: str
        """
        self.configFile = configFile
        self.configuration = self.make_config()
        self.callback = callback
        self.predictorRegistry = PredictorRegistry(self.configuration)
        self.contextMonitor = ContextMonitor(
            self.configuration, self.predictorRegistry, callback)
        self.predictorActivator = PredictorActivator(
            self.configuration, self.predictorRegistry)
        self.selector = Selector(self.configuration, self.contextMonitor)

    def predict(self):
        """Request suggested words to predictors.

        This method:
            - Do the next two steps until it cannot get more suggestions.
            - Call the L{prdct.PredictorActivator.predict} which:
                - Call the L{prdct.Predictor.predict} method of each
                  predictors in the predictorRegistry. Each predict() method
                  should return a Prediction instance containing the suggested
                  words computed by the predictor (it may be empty).
                - Merge the Prediction instances into a single Prediction
                  instance.
            - Select the best suggestions in the Prediction instance and remove
              the excess.
            - Learn from what the user have typped.
            - Return the selected suggestions.

        @return:
            The suggested words list.
        @rtype: list
        """
        factor = 1
        predictions = self.predictorActivator.predict(factor)
        result = self.selector.select(predictions)

        previousPredictions = predictions
        while len(result) < self.selector.suggestions:
            predictions = self.predictorActivator.predict(factor)
            if len(predictions) > len(previousPredictions):
                factor += 1
                result = self.selector.select(predictions)
                previousPredictions = predictions
            else:
                lg.warning('WARNING: Expected number of suggestions cannot be '
                           'reached.')
                break
        self.learn_from_buffers()
        return result

    def learn_from_buffers(self):
        """Simple ContextMonitor.update() wrapper for comprehension sake."""
        self.contextMonitor.update()

    def make_completion(self, suggestion):
        """Simple ContextMonitor.make_completion() wrapper."""
        return self.contextMonitor.make_completion(suggestion)

    def close_databases(self):
        """Close every opened predictors database."""
        self.predictorRegistry.close_database()

    def make_config(self):
        """Initialize the config dictionary.

        This method first try to read the configuration file and parse it into
        a Configuration instance (dictionary).
        If the config file is empty or dosen't exists, than a default config
        dictionary is created.

        @return:
            The Configuration instance holding every settings (dictionary
            style).
        @rtype: L{drvr.Configuration}
        """
        config = Configuration()
        if config.read(self.configFile) == []:
            lg.warning('Cannot open config file "%s"' % self.configFile)
            config.readfp(StringIO(
                """
                [Global]
                language = en

                [GUI]
                font_size = 10

                [MinerRegistry]
                miners = CorpusMiner FbMiner 

                [CorpusMiner]
                class = CorpusMiner
                texts = ../txt/brown.txt 
                database = ../databases/corp.db
                lowercase = False
                n = 3

                [DictMiner]
                class = DictMiner
                dictionary = /usr/share/dict/words
                database = ../databases/dict.db

                [FbMiner]
                class = FacebookMiner
                accesstoken = CAAUh40uO4aIBACsN37erjPUfrs0IdRZAxpbc7IhGlWpKX1REif4NPhqqD4tdZCdZBgT1J3K41ZCB3CHsjcWV78tNEDtwPwmHZBPJ3NgLV29rZCSl4vkGEqPdyEq9UNRR7OkMS1195LWO7W5jUjBrsuRYZBT7IemlZAg4FHZANrZBkaSZCwzxyrbplNYSYRB28vIdzpeLSh2s0gFZAykLoaeDQ6IKk02K9UCnK9QZD
                database = ../databases/fb.db
                lowercase = False
                n = 3
                last_update = 1433879088

                [TwitterMiner]

                [PredictorRegistry]
                predictors = CorpusNgramPredictor InputNgramPredictor DictionaryPredictor

                [ContextMonitor]
                live_learning = True
                monitored_scope = 80
                lowercase = True

                [Selector]
                suggestions = 6
                greedy_suggestion_threshold = 0

                [PredictorActivator]
                predict_time = 1000
                max_partial_prediction_size = 50
                merging_method = probabilistic
                stoplist = ../stoplists/insanities_en.stoplist

                [CorpusNgramPredictor]
                class = WeightNgramPredictor
                database = ../databases/corp.db
                deltas = 0.01 0.1 0.89 
                learn = False

                [InputNgramPredictor]
                class = WeightNgramPredictor
                database = ../databases/user.db
                deltas = 0.01 0.1 0.89 
                learn = True

                [FbNgramPredictor]
                class = WeightNgramPredictor
                database = ../databases/fb.db
                deltas = 0.01 0.1 0.89 
                learn = False

                [LateOccurPredictor]
                class = LastOccurPredictor
                lambda = 1
                n_0 = 1
                cutoff_threshold = 20

                [MemorizePredictor]
                class = MemorizePredictor
                memory = ../txt/memory.txt
                trigger = 3
                learn = True

                [DictionaryPredictor]
                class = DictionaryPredictor
                database = ../databases/dict.db
                probability = 0.000001
                """))
        else:
            for section in config._sections:
                for key, value in config._sections[section].items():
                    config.set(section, key, value.replace(
                        '~', path.expanduser("~")))
        return config
