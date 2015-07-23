"""
Programmer: JR Padfield
Description: Tool to help you save things in binary
Version: 1
Date:
"""

import configparser
import os

class ini:
    """ Saves and reads information into binary format """

    def putvar(self, filename, header, var, value):
        """ Puts information into a ini file """
        if not os.path.isfile(filename):
            cfgfile = open(filename, 'w')
        else:
            cfgfile = open(filename, 'w')

        # Lets add information to the file
        config = configparser.ConfigParser()
        config.add_section(header)
        config.set(header, var, value)
        config.write(cfgfile)
        cfgfile.close()

    def getvar(self, filename, header, var):
        """ Gets the information of a certain variable of the ini file """
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(filename)
        return config.get(header, var)
