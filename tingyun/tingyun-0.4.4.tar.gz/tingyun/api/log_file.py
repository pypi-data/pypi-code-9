import sys
import logging
import logging.handlers
import threading


"""used to define and handle the hole agent log
"""

_lock = threading.Lock()
_agent_logger = logging.getLogger('tingyun')
_LOG_FORMAT = '%(asctime)s (%(process)d/%(threadName)s) %(name)s %(lineno)s %(levelname)s - %(message)s'
_initialized = False


class _NullHandler(logging.Handler):
    def emit(self, record):
        pass

_agent_logger.addHandler(_NullHandler())


def _initialize_stdout_logging(log_level):
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(_LOG_FORMAT)
    handler.setFormatter(formatter)

    _agent_logger.addHandler(handler)
    _agent_logger.setLevel(log_level)

    _agent_logger.info('Initializing Python agent stdout logging.')


def _initialize_stderr_logging(log_level):
    handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter(_LOG_FORMAT)
    handler.setFormatter(formatter)

    _agent_logger.addHandler(handler)
    _agent_logger.setLevel(log_level)

    _agent_logger.info('Initializing Python agent stderr logging.')


def _initialize_file_logging(log_file, log_level):
    handler = logging.FileHandler(log_file)
    # backup the log by day and the max days is 10
    # handler = logging.handlers.TimedRotatingFileHandler(log_file, 'd', 1, 10)

    formatter = logging.Formatter(_LOG_FORMAT)
    handler.setFormatter(formatter)

    _agent_logger.addHandler(handler)
    _agent_logger.setLevel(log_level)
    _agent_logger.propagate = False

    _agent_logger.info('Log file "%s".' % log_file)


def initialize_logging(log_file, log_level):
    global _initialized

    if _initialized:
        return 1

    _lock.acquire()
    try:
        if log_file == 'stdout':
            _initialize_stdout_logging(log_level)

        elif log_file == 'stderr':
            _initialize_stderr_logging(log_level)

        elif log_file:
            try:
                _initialize_file_logging(log_file, log_level)
            except Exception as _:
                _initialize_stderr_logging(log_level)
                _agent_logger.exception('Falling back to stderr logging as unable to create log file %r.' % log_file)

        _initialized = True
    finally:
        _lock.release()
        return 0
