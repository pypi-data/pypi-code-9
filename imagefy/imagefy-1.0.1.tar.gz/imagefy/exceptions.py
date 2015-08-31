class ImagefyException(Exception):
    pass


class ImagefyOperationException(ImagefyException):
    def __init__(self, message, operation, original_exc=None):
        super(ImagefyOperationException, self).__init__(message)
        self.operation = operation
        self.original_exc = original_exc