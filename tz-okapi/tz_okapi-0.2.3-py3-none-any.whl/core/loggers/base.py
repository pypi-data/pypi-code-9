class BaseLogger(object):
    """
    Abstract class to provide logging facilities.

    Methods:

    - write
    - info
    - success
    - warning
    - error

    """

    verbosity = 0

    LEVEL_INFO = 3
    LEVEL_SUCCESS = 3
    LEVEL_WARNING = 2
    LEVEL_ERROR = 2

    def write(self, s, *args, **kwargs):
        """
        Implementation of write method.

        :param s: String output
        :type s: str
        """
        raise NotImplementedError

    def info(self, s, *args, **kwargs):
        """
        :type s: str
        """
        if self.verbosity >= self.LEVEL_INFO:
            return self.write(s, *args, **kwargs)

    def success(self, s, *args, **kwargs):
        """
        :type s: str
        """
        if self.verbosity >= self.LEVEL_SUCCESS:
            return self.write(s, *args, **kwargs)

    def warning(self, s, *args, **kwargs):
        """
        :type s: str
        """
        if self.verbosity >= self.LEVEL_WARNING:
            return self.write(s, *args, **kwargs)

    def error(self, s, *args, **kwargs):
        """
        :type s: str
        """
        if self.verbosity >= self.LEVEL_ERROR:
            return self.write(s, *args, **kwargs)
