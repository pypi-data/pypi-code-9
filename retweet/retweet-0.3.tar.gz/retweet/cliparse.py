# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# CLI parsing
'''CLI parsing'''

import os.path
import sys

class CliParse(object):
    '''CliParse class'''
    def __init__(self):
        '''Constructor for the CliParse class'''
        self.pathtoconf = sys.argv[-1]
        self.main()

    def main(self):
        '''main of CliParse class'''
        # checks for the path to the configuration
        if self.pathtoconf.endswith('retweet.py') or self.pathtoconf.endswith('retweet'):
            print('No config file was provided. Exiting.')
            sys.exit(0)
        if not os.path.exists(self.pathtoconf):
            print('the path you provided for yaspe configuration file does not exists')
            sys.exit(1)
        if not os.path.isfile(self.pathtoconf):
            print('the path you provided for yaspe configuration is not a file')
            sys.exit(1)
        self.validpathtoconf = self.pathtoconf

    @property
    def configfile(self):
        '''return the path to the config file'''
        return self.validpathtoconf
