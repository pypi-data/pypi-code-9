

class TOMLError(Exception):
    """
    All errors raised by this module are descendants of this type.
    """


class InvalidTOMLFileError(TOMLError):
    pass


class NoArrayFoundError(TOMLError):
    """
    An array of tables was requested but none exist by the given name.
    """


class InvalidValueError(TOMLError):
    pass
