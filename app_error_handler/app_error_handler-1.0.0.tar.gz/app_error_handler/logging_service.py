import json
from logging import WARN, ERROR, CRITICAL
from app_error_handler.interfaces.logging_service_interface import LoggingServiceInterface


class LoggingService(LoggingServiceInterface):

    def __init__(self, logger):
        self.app_logger = logger
        self._logging_level_fn = {WARN: self.app_logger.warning, ERROR: self.app_logger.error,
                                  CRITICAL: self.app_logger.critical}

    def log_error(self, log_level_fn, error_details, request, stack_trace):
        error_details = dict(error_details)
        error_details['trace_stack'] = stack_trace
        self._log_request_data(request)
        fn = self._logging_level_fn.get(log_level_fn, self.app_logger.critical)
        fn(json.dumps(error_details))

    def _log_request_data(self, request):
        try:
            self.app_logger.info(u"Request data given to application:\n {}".format(request.data))
        except (AttributeError, RuntimeError) as e:
            self.app_logger.debug(u"Could not log request data. Error info: {}".format(e))
