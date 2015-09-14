from abc import ABCMeta, abstractmethod


class LoggingServiceInterface():

    __metaclass__ = ABCMeta

    @abstractmethod
    def log_error(self, log_level_fn, error_details, request, stack_trace):
        '''
        log_level_fn - is the logging function from Logger, can be one of warning, error or critical
        error_details - is a dictionary contain information of about the error condition
        request - is the request object
        stack_trace - can be either a full stack trace or partial
        '''
        pass # pragma: no cover


