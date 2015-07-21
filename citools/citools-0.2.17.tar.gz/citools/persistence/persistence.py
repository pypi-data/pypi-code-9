import shelve


class Persistence(object):
    REPORT_KEY = 'report'

    def __init__(self, name):
        self.name = name
        self.shelve = shelve.open(name)

    def get_report(self):
        return self.shelve.get(self.REPORT_KEY)

    def set_report(self, report):
        self.shelve[self.REPORT_KEY] = report

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.shelve.close()
