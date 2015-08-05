class OkapiException(Exception):
    """
    Base exception of okapi package. Should be use for every custom
    exception class.
    """
    pass


class InvalidHeaderException(OkapiException):
    pass
