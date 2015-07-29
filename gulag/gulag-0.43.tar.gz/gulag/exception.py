class DatabaseNotFoundError(Exception):
    """
    """
class SessionNotActive(Exception):
    """
    """

class MongoConnectionLost(Exception):
    """
    Raised after maximum number of retries has been exceeded
    settings.NUM_MONGO_AUTO_CONNECT_RETRY
    """

class MissingHost(Exception):
    """
    Raised after mongo model initialised without 'host' parameter
    """

class MissingCollectionName(Exception):
    """
    Raised after mongo model initialised without 'col_name' parameter
    """

class UserForbidden(Exception):
    """
    Raised when API auth fails
    """

class PathNotFound(Exception):
    """
    Raised when trying to output to a non-existant file
    """

class QueueNotFound(Exception):
    """
    Raised when queue check fails
    """

class OverSizeLimit(Exception):
    """
    Raised when API attempt to upload a file larger than settings.MAXIMUM_DOC_SIZE_K
    """

class TaskNotReady(Exception):
    """
    Raise when trying to get OCR result from a task not finished
    """

class TaskResultInvalid(Exception):
    """
    Raised when task result is empty
    """

class ConfigError(Exception):
    """
    """

class PathNotFound(Exception):
    """
    """