from exceptions import Exception


class ApiException(Exception):
    """
    General API exception
    """
    def __init__(self, message=None, *args, **kwargs):
        self.__dict__.update(kwargs)
        if message:
            self.message = message

    @property
    def as_json(self):
        return self.__dict__


class AuthorizationError(Exception):

    def __init__(self, name='', *args, **kwargs):
        self.name = name
        super(AuthorizationError, self).__init__(*args, **kwargs)


class MethodNotAllowedError(Exception):

    def __init__(self, method='', *args, **kwargs):
        self.method = method
        super(MethodNotAllowedError, self).__init__(*args, **kwargs)


class PreConditionError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class SavoryPieError(Exception):
    """
    General Savory Pie Error
    """
    pass
