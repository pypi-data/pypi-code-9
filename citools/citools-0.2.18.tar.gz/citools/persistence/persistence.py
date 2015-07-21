import shelve


class Persistence(object):
    REPORT_KEY = 'report'
    SOURCE_JOBS_KEY = 'source_jobs'

    def __init__(self, name):
        self.name = name
        self.shelve = shelve.open(name)

    @property
    def report(self):
        return self.shelve.get(self.REPORT_KEY)

    @report.setter
    def report(self, report):
        self.shelve[self.REPORT_KEY] = report

    @property
    def source_jobs(self):
        return self.shelve.get(self.SOURCE_JOBS_KEY)

    @source_jobs.setter
    def source_jobs(self, source_jobs):
        self.shelve[self.SOURCE_JOBS_KEY] = source_jobs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.shelve.close()
