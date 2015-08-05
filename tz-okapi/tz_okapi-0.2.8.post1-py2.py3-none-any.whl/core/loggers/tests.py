from okapi.core.loggers.base import BaseLogger


class TestLogger(BaseLogger):
    """
    Logger for tests, doesn't output anything, just stores logs into buffer.
    """

    def __init__(self):
        self.buffer = []
        """
        List of logs.

        :type: list[str]
        """

    def write(self, s, *args, **kwargs):
        self.buffer.append(s.strip())
