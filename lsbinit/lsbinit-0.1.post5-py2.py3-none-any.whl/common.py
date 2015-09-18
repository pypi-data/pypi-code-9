from os import makedirs, path
from sys import stderr, stdout, exit, version_info

class _LSBCommon(object):
    """
    Shared class for LSB handler classes.
    """
    def die(self, msg, code=1):
        stderr.write('{}\n'.format(msg))
        exit(code)

    def unicode(self, string):
        """
        Make sure a string is unicode across Python2/Python3
        """
        try:
            return str(string, 'utf-8')
        except TypeError:
            return string

    def write_stdout(self, msg, code=None):
        stdout.write('{}\n'.format(msg))
        if code:
            exit(code)
            
    def mkdir(self, dir, mode=755):
        if not path.isdir(dir):
            makedirs(dir, mode)
        return dir
        
    def mkfile(self, file, contents=None, mode='w'):
        file_handle = open(file, mode)
        if contents:
            file_handle.write(contents)
        file_handle.close()
        return file