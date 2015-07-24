

class DatasetError(Exception):

    NOT_FOUND = 1

    def __init__(self, type, message):
        self.type = type
        self.message = message
