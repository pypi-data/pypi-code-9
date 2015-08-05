import termios
import sys
import tty
import select


def count_lines(file_name):
    """

        Counts how many lines has a the given file

    :param file_name: A file path
    :return: Number of lines of the file (0 for empty files)
    """
    lines = 0
    with open(file_name, 'rb') as f:
        for line in f:
            lines += 1

    return lines


class NonBlockingConsole(object):

    def __init__(self, interactive=True):
        self.interactive = interactive

    def __enter__(self):

        if self.interactive:
            try:
                self.old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            except Exception:
                self.enable = False
            else:
                self.enable = True
        else:
            self.enable = False

        return self

    def __exit__(self, type, value, traceback):
        if self.enable:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if self.enable and select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False
