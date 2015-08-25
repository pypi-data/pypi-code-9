import os.path
import sys

class CliParse(object):
    '''CliParse class'''
    def __init__(self):
        '''Constructor for the CliParse class'''
        pathtoconf = sys.argv[-1]
        # checks for the path to the configuration
        if pathtoconf.endswith('retweet.py') or pathtoconf.endswith('retweet'):
            print('No config file was provided. Exiting.')
            sys.exit(0)
        if not os.path.exists(pathtoconf):
            print('the path you provided for yaspe configuration file does not exists')
            sys.exit(1)
        if not os.path.isfile(pathtoconf):
            print('the path you provided for yaspe configuration is not a file')
            sys.exit(1)
        self.pathtoconf = pathtoconf

    @property
    def configfile(self):
        '''return the path to the config file'''
        return self.pathtoconf
