from sys import stderr, stdout, exit

class _LSBCommon(object):
    """
    Shared class for LSB handler classes.
    """
    def die(self, msg, code=1):
        stderr.write('{}\n'.format(msg))
        exit(code)

    def write_stdout(self, msg, code=None):
        stdout.write('{}\n'.format(msg))
        if code:
            exit(code)