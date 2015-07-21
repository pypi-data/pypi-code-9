

class Summary(object):
    def __init__(self):
        self.count = 0
        self.failed = 0
        self.failed_tests = []
        self.time_start = None
        self.time_end = None

    @property
    def time_elapsed(self):
        return self.time_end - self.time_start
