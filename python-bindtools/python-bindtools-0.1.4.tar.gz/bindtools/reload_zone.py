__author__ = 'Scott Godbold'

import subprocess


# --------------------------- #
# -------- Exceptions ------- #
# --------------------------- #
class RNDCFreezeException(Exception):
    pass


class RNDCThawException(Exception):
    pass


class RNDCReloadException(Exception):
    pass


# --------------------------- #
# --------- Classes --------- #
# --------------------------- #
class ReloadZone(object):
    """Wraps rndc utility to utilize reloading zones"""
    def __init__(self, rndc='rndc'):
        super(ReloadZone, self).__init__()
        self.rndc = rndc

    def freeze(self, path):
        """Freezes a dynamic zone"""
        cmd = '{} freeze {}'.format(self.rndc, path)
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None,
                                    shell=True)

        # Again formating is strange
        message = response.communicate()[0].decode(encoding='windows-1252')

        if response.returncode != 0:
            raise RNDCFreezeException(message)

        return True

    def thaw(self, path):
        """Freezes a dynamic zone"""
        cmd = '{} thaw {}'.format(self.rndc, path)
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None,
                                    shell=True)

        # Again formating is strange
        message = response.communicate()[0].decode(encoding='windows-1252')

        if response.returncode != 0:
            raise RNDCThawException(message)

        return True

    def reload(self, path):
        """Freezes a dynamic zone"""
        cmd = '{} reload {}'.format(self.rndc, path)
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None,
                                    shell=True)

        # Again formating is strange
        message = response.communicate()[0].decode(encoding='windows-1252')

        if response.returncode != 0:
            raise RNDCReloadException(message)

        return True
