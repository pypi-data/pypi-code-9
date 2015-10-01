# Copyright (C) 2014
# Institut d'Astrophysique Spatiale
#
# Forked from the BoA project
#
# Copyright (C) 2002-2006
# Max-Planck-Institut fuer Radioastronomie Bonn
# Argelander Institut fuer Astronomie
# Astronomisches Institut der Ruhr-Universitaet Bochum
#
# Produced for the LABOCA project
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Library General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Library General Public License for more
# details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#

"""
..modules:: ReaMessageHandler
:synopsis: contains the Rea message handler class
"""
__version__ = '$Revision: 2195 $'
__date__ = '$Date: 2007-07-15 16:45:11 +0200 (dim, 15 jui 2007) $'

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#-------------------------------------------------------------------------
import os
import sys
import string
import time
from rea import ReaConfig

# Keeps all the messages in memory
_history = {}  # for test


def printHistory():
    allkeys = sorted(_history.keys())

    for key in allkeys:
        print key, _history[key]

#----------------------------------------------------------------------------------
#----- Rea Message Handler --------------------------------------------------------
#-------------------------------------------------------------------------


class MessHand:

    """..class:: MessHand
    :synopsis: An object of this class is responsible for the management of output
    messages as well as the creation of message files.
    """

    def __init__(self, logName='Unknown'):
        """initialise an instance

        Parameters
        ----------
        logName : str
            the filename of the logfile
        """

        # parameter attributes:

        # default value for max. weight of messages to be printed
        self.maxWeight = ReaConfig.maxMessHandWeight

        # Private attributes:

        self.__logName = ''  # Name of the class using the Message Handler
                            # 20 char long left hand stripped.
        self.__WeightList = {
            1: 'E:',
            2: 'W:',
            3: 'I:',
            4: 'L:',
            5: 'D:'}  # list of allowed weights
        self.__WeightDescription = ['errors', 'warnings',
                                    'short info', 'extended info',
                                    'debug']

        self.__messFileName = "rea.mes"                                   # default name of message file
# self.__prompt = chr(1) + "\033[1;32m" + chr(2) + 'rea>' + chr(1) +
# "\033[0m" + chr(2)
        self.__prompt = 'rea<'

        # methods to run at initialisation
        self.setLogName(logName)

    def __del__(self):
        self.debug("closing message handler '" + self.__logName.strip() + "'")

    #--------------------------------------------------------------------------------
    #----- methods ------------------------------------------------------------------
    #-------------------------------------------------------------------------
    def Welcome(self):
        """print welcome message"""
        str = ""
        print
        print " Welcome to The REceiver Array data Analysis project ! "
        print "   -------------------------------------------    "

        if os.environ.get('USER'):
            str += " User: " + os.environ.get('USER') + " "
        str += "(" + time.ctime() + ")\n"
        #   str += "Running on " +sys.platform+" with Python "+sys.version
        print str

    #-------------------------------------------------------------------------
    def setMaxWeight(self, weight='2'):
        """Set the maximum weight of messages to be printed.

        Parameters
        ----------
        weight : int
            maximum weight
                      1: errors, queries
                      2: warnings
                      3: short info
                      4: extended info
                      5: debug
        """
        if weight in self.__WeightList:
            self.maxWeight = weight
            self.info("max weight of messages = " + repr(self.maxWeight))
        else:
            self.error("invalid max weight of messages: " + repr(weight))

    #-------------------------------------------------------------------------
    def setLogName(self, logName='Unknown'):
        self.__logName = logName.ljust(20)    # Name of the class using
        self.__logName = self.__logName[0:20]  # the Message Handler 20 char
                                              # long left hand stripped

    #-------------------------------------------------------------------------
    def pause(self, message=''):
        """allow to make a pause in the program

        Parameters
        ----------
        message : str
            a message to display
        """
        if not message:
            message = 'Please press enter to continue'

        self.ask(message)

    #-------------------------------------------------------------------------
    def yesno(self, message=''):
        """ask the user a question with yes/no answer type

        Parameters
        ----------
        message : str
            the question

        Returns
        -------
        bool
            the answer
        """

        yes = ['y', 'Y', 'yes', 'Yes', 'YES']
        no = ['n', 'N', 'no', 'No', 'NO']
        answer = ''
        while answer not in yes and answer not in no:
            answer = self.ask(message + ' (y/n): ')

        if answer in yes:
            return 1
        else:
            return 0

    #-------------------------------------------------------------------------
    def ask(self, message=''):
        """ask the user

        Parameters
        ----------
        message : str
            the question

        Returns
        -------
        str
            the answer
        """
        return raw_input(self.__prompt + ' ?: ' + message)

    #-------------------------------------------------------------------------
    def error(self, message=''):
        """to print an error message

        Parameters
        ----------
        message : str
            the error message
        """
        self.setMess(1, message)

    #-------------------------------------------------------------------------
    def warning(self, message=''):
        """to print an warning message

        Parameters
        ----------
        message : str
            the warning message
        """
        self.setMess(2, message)

    #-------------------------------------------------------------------------
    def info(self, message=''):
        """to print an info message

        Parameters
        ----------
        message : str
            the info message
        """
        self.setMess(3, message)

    #-------------------------------------------------------------------------
    def longinfo(self, message=''):
        """to print an long info message

        Parameters
        ----------
        message : str
            the long information message
        """
        self.setMess(4, message)

    #-------------------------------------------------------------------------
    def debug(self, message=''):
        """to print an debug message

        Parameters
        ----------
        message : str
            the debug message
        """
        self.setMess(5, message)

    #-------------------------------------------------------------------------
    def line(self):
        """to print a line"""
        message = '-' * (80 - 10)
        self.setMess(4, message)

    #-------------------------------------------------------------------------
    def setMess(self, weight=1, message=' '):
        """deposit messages for screen output and message files

        Parameters
        ----------
        weight : int
            weight of transferred message (see setMaxWeight)
              1 - error
              2 - warning
              3 - info
              4 - longinfo
              5 - debug
        message : str
            message to be printed and added to message file
        """
        if weight in self.__WeightList:
            message = message.strip()
            short_prefix = " " + self.__WeightList[weight] + " "
            long_prefix = time.ctime() + " " + self.__logName + short_prefix

            if weight <= self.maxWeight:                         # Print if asked ...

                # ... in file
                if (self.__messFileName != ""):
                    messFile = open(self.__messFileName, 'a')
                    for line in message.split('\n'):
                        messFile.write(long_prefix + line + "\n")
                    messFile.close()
                    del messFile
                else:

                    print self.__prompt + " " + self.__WeightList[1] + " " + \
                        "the log file for this message handler is closed or undefined"

                # ... on screen
                for line in message.split('\n'):
                    print self.__prompt + short_prefix + line

                # and add this to history
                _history[long_prefix] = message

                del short_prefix, long_prefix

    #-------------------------------------------------------------------------
    def initMessFile(self, filename="rea.mes"):
        """set & initialise new message file

        Parameters
        ----------
        filename : str
            log filename
        """

        if self.__messFileName == "":
            self.__messFileName = os.path.join(
                ReaConfig.outDir, filename.strip())

        try:

            if os.path.isfile(self.__messFileName):
                # File name already exist so move it to a new location
                # First find a available file name as self.__messFileName+i
                i = 1
                while(os.path.isfile(self.__messFileName + str(i))):
                    i += 1
                newFileName = self.__messFileName + str(i)
                self.info('old log file renamed to ' + newFileName)
                os.rename(self.__messFileName, newFileName)

            messFile = open(self.__messFileName, 'w')
            messFile.write(
                "Logfile for The REceiver Array data Analysis project. ")
            messFile.write("created on " + time.ctime() + "\n")
            messFile.close()
            del messFile

        except IOError:
            self.error("cannot open message file " + self.__messFileName)

    #-------------------------------------------------------------------------
    def closeMessFile(self):
        """set self.__existMessFile to 0 and file name to ""
        """
        self.debug("closing message file " + self.__messFileName)
        self.__messFileName = ""

#----------------------------------------------------------------------------------
#----- For compatibility with the CalibratorLog class -----------------------------
#-------------------------------------------------------------------------


class Logger:

    """..class:: Logger
    :synopsis: for compatiliby with the CalibratorLog.Logger class
    """

    def __init__(self, logType='ACS'):
        """Initiabise an instance"""

        self.logger = printLogger()


class printLogger(MessHand):

    """..class:: printLogger
    :synopsis: for compatibility with the CalibratorLog.printLogger class
    """

    def __init__(self):

        MessHand.__init__(self)
        self.setLogName(logName='CalibratorLog')

    #--------------------------------------------------------------------------------
    # Compatibility with the CalibratorLog class
    def logInfo(self, message):
        self.info(message)

    def logError(self, message):
        self.error(message)

    def logWarning(self, message):
        self.warning(message)

    def logDebug(self, message):
        self.debug(message)
