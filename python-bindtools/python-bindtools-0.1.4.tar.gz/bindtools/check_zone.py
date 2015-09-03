__author__ = 'Scott Godbold'

import subprocess


# Exceptions
class CheckZoneException(Exception):
    def __init__(self, messages):
        self.message = str(messages)

    def __str__(self):
        return self.message


# Classes
class CheckZone(object):
    """Wraps the named-checkzone utility and allows you to easily check zone
    file syntax"""
    def __init__(self, checkzone='named-checkzone'):
        super(CheckZone, self).__init__()
        self.checkzone = checkzone

    def validate(self, zone_name, path):
        """docstring for validate"""
        cmd = '{} {} {}'.format(self.checkzone, zone_name, path)
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=None, shell=True)

        # This seems wrong but works anyway, may wanna look into it later
        messages = response.communicate()[0].decode(encoding='windows-1252')

        if response.returncode != 0:
            raise CheckZoneException('Zone build failed for bad syntax:\n{}'.format(messages))
        return True
