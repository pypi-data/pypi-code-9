class FileNotFoundError(Exception):
    def __init__(self, message):
        super().__init__("File is not found:"+message)

class EmptyFileError(Exception):
    def __init__(self, message):
        super().__init__("File is empty:"+message)

class EmptyArticleError(Exception):
    def __init__(self, message):
        super().__init__("Article is empty:"+message)

class RequiredValueMissing(Exception):
    def __init__(self, message):
        super().__init__("Required value "+message+" was missing")
