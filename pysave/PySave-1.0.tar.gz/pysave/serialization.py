"""
Programmer: JR Padfield
Description: Tool to help you save things in pickle serialization
Version: 1
Date:
"""

import pickle

class serialize:
    """ Saves information as json encoding. """

    def savedata(self, data, filename):
        """ Saves the data to a file through json """
        pickle.dump(data, open(filename, 'wb'))

    def loaddata(self, filename):
        """ Loads the data from the file """
        return pickle.load(open(filename, 'rb'))


