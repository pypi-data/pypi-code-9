import logging


class ConfigError(Exception):
    def __init__(self, message, errors=None):
        super(ConfigError, self).__init__(message)

        self.errors = errors
        logging.error(message)


class SearchException(Exception):
    def __init__(self, message, errors=None):
        super(SearchException, self).__init__(message)
        logging.error(message)


class SearchEmptyException(Exception):
    def __init__(self, message):
        super(SearchEmptyException, self).__init__(message)
        logging.error(message)


class AmqpParseException(Exception):
    def __init__(self, message, errors=None):
        super(AmqpParseException, self).__init__(message)


class CrawlException(Exception):
    def __init__(self, message, errors=None):
        super(CrawlException, self).__init__(message)