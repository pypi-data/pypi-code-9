class File:
    def __init__(self, filename):
        self.filename = filename

    def is_hidden_file(self):
        return self.filename.startswith('.') or self.filename.endswith('~')

    @property
    def year(self):
        return self.filename[:4]

    @property
    def month(self):
        return self.filename[5:7]

    @property
    def day(self):
        return self.filename[8:10]

    @property
    def title(self):
        return self.filename[11:-3]

    @property
    def info(self):
        return [self.year, self.month, self.day, self.title]
