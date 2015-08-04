from __future__ import print_function
from colorama import Back, Fore, Style

from okapi.core.loggers.base import BaseLogger


class Console(BaseLogger):
    """
    Writes logs directly to console.
    """

    def write(self, s, *args, **kwargs):
        """
        :type s: str
        """
        print(s, **kwargs)


class ColoredConsole(Console):
    """
    Extends simple ``Console`` class and adds fancy colors to output.
    """
    RESET = Back.RESET + Fore.RESET + Style.RESET_ALL

    def write(self, s, *args, **kwargs):
        """
        :type s: str
        """
        super(ColoredConsole, self).write(
            ''.join(args) + s + self.RESET, **kwargs
        )

    def success(self, s, *args, **kwargs):
        """
        :type s: str
        """
        return super(ColoredConsole, self) \
            .success(s, Fore.GREEN, *args, **kwargs)

    def info(self, s, *args, **kwargs):
        """
        :type s: str
        """
        return super(ColoredConsole, self).info(s, Fore.BLUE, *args, **kwargs)

    def warning(self, s, *args, **kwargs):
        """
        :type s: str
        """
        return super(ColoredConsole, self) \
            .warning(s, Fore.YELLOW, *args, **kwargs)

    def error(self, s, *args, **kwargs):
        """
        :type s: str
        """
        return super(ColoredConsole, self).error(s, Fore.RED, *args, **kwargs)
