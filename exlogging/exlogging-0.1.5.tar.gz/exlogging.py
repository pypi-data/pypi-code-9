import pkg_resources
import logging.handlers
import types
from logging import *  # noqa


def _init_package():
    try:
        return pkg_resources.get_distribution('exlogging').version
    except:
        return "Please install this project with setup.py"

__version__ = _init_package()

log_levels = {
    'critical': CRITICAL,
    'error': ERROR,
    'warning': WARNING,
    'info': INFO,
    'debug': DEBUG,
    'notset': NOTSET,
}
default_log_format = Formatter(
    '%(levelname)s %(name)s - %(asctime)s - File: %(pathname)s - Line: %(lineno)d'
    '- Func: %(funcName)s Message: %(message)s'
)


def init(config: dict, name: str=None) -> Logger:
    def create_handler(function: types.FunctionType, config: dict) -> Handler:
        if config is None:
            return None

        handler = function(config)
        handler.setLevel(log_levels[config['level']])
        handler.setFormatter(config.get('log_format', default_log_format))
        return handler

    def create_file_hander() -> Handler:
        return create_handler(
            lambda config: FileHandler(filename=config['filename'], encoding='UTF-8'),
            config.get('file')
        )

    def create_email_handler() -> Handler:
        return create_handler(lambda config: logging.handlers.SMTPHandler(
            mailhost=(config['smtp_host'], config['smtp_port']),
            fromaddr=config['email_from'],
            toaddrs=(config['email_to'], ),
            subject=config['email_subject'],
            credentials=(config['smtp_username'], config['smtp_password']),
            secure=()
        ), config.get('email'))

    def create_rotating_file_handler() -> Handler:
        """See: https://docs.python.org/3.5/library/logging.handlers.html#rotatingfilehandler"""
        return create_handler(lambda config: logging.handlers.RotatingFileHandler(
            filename=config['filename'],
            maxBytes=config.get('max_bytes', 0),
            backupCount=config.get('backup_count', 0)
        ), config.get('rotating_file'))

    logger = getLogger(name)
    logger.setLevel(NOTSET)

    for function in [create_file_hander, create_email_handler, create_rotating_file_handler]:
        hundler = function()
        if hundler is not None:
            logger.addHandler(hundler)

    return logger
