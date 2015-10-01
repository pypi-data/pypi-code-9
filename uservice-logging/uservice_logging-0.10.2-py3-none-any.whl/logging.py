# uservice-logging
# Copyright (C) 2015 Canonical
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Code to configure logging for micro-services."""

import collections
import datetime
import json
import logging
import logging.handlers
import logstash
import os
import socket
import threading

__all__ = [
    'configure_service_logging'
]

_logging_configured = []


class SafeEncoder(json.JSONEncoder):
    """A JSON encoder that never fails to encode a field."""
    def default(self, obj):
        # try to get nice formatting for known types
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        # fallback to just get object's repr
        try:
            return repr(obj)
        except:
            # but if repr fails, just get its info at 'object' level
            return "<<Unrepresentable: {} >>".format(object.__repr__(obj))


def safe_serializer(message):
    dumped = json.dumps(message, cls=SafeEncoder)
    return dumped.encode('utf8')


def configure_logging(config, service, level=logging.INFO, **kwds):
    """Simplified setup for the micro-service logging.

    If present config['logstash'] is used to setup logstash (see
    configure_service_logging), service and optional kwds are passed as
    logstash entries.

    The log path is set to <LOG_DIR>/<service>.log assuming LOG_DIR is
    set in the environment.
    """
    # avoid duplicate logging
    if _logging_configured:
        return
    _logging_configured.append(True)

    if 'hostname' not in kwds:
        kwds['hostname'] = socket.gethostname()
    kwds['service'] = service

    class _LogstashExtraLogger(ExtraLogger):
        prefix = 'spi.'
        extra_args = kwds
    logging.setLoggerClass(_LogstashExtraLogger)

    log_path = None
    if 'LOG_DIR' in os.environ:
        log_path = os.path.join(os.environ['LOG_DIR'], service + '.log')

    logstash_config = None
    if 'logstash' in config:
        logstash_config = config['logstash']
    return configure_service_logging(log_path, logstash_config, level)


def configure_service_logging(log_file_path=None, logstash_config=None, level=logging.INFO):
    """Configure python's logging for the micro-service.

    This function sets a standard level of logging for all our services. The
    default setups is to log to a file, or stderr if the file directory cannot
    be created.

    Additionally, if the logstash config is supplied, a logstash handler will
    be configured.

    :param log_file_path: The full path to a file to be used for logging. If
        the file's directory does not exist, this function will fall back to
        logging to stderr instead of the file.
    :param logstash_config: If specified, must be a mapping type that contains
        the keys 'host', 'port', and 'version'.
    :param level: The logger level (default to INFO).

    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Silence requests logging, which is created by nova, keystone and swift.
    requests_logger = logging.getLogger('requests')
    requests_logger.setLevel(logging.WARNING)

    # If there is no .directory for the file, fall back to stderr logging
    if log_file_path:
        if os.path.exists(os.path.dirname(log_file_path)):
            handler = logging.handlers.TimedRotatingFileHandler(
                log_file_path,
                when='D',
                interval=1
            )
        else:
            print("parent directory for log '{}' does not exist, using stderr "
                  "for app log.".format(log_file_path))
            handler = logging.StreamHandler()
    else:
        print("No log file path given, using stderr for app log.")
        handler = logging.StreamHandler()

    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s  %(name)s %(levelname)s: %(message)s'
        )
    )
    root_logger.addHandler(handler)

    if logstash_config:
        handler = logstash.LogstashHandler(
            logstash_config['host'],
            int(logstash_config['port']),
            version=int(logstash_config['version'])
        )
        # monkeypatch the serializer in the handler's formatter to
        # use the own safe serializer
        handler.formatter.serialize = safe_serializer
        root_logger.addHandler(handler)


class ExtraLogger(logging.Logger):

    """A logger that handles passing 'extra' arguments to all logging calls.

    Tired of having to write:

    logger.info("Some message", extra=extra)

    ... everywhere?

    Now you can install this class as the Logger class:

    >>> import logging
    >>> logging.setLoggerClass(ExtraLogger)

    Then, to use it, get your logger as usual:

    >>> logger = logging.getLogger(__name__)

    ...and set your extra arguments once only:

    >>> logger.set_extra_args(dict(foo='bar', baz='123'))

    And those arguments will be included in all normal log messages:

    >>> logger.info("Hello World") # message will contain extra args set above

    Alternatively extra arguments can be attached to a subclass:

    >>> class XLogger(ExtraLogger):
    >>>     extra_args = dict(foo='bar', baz='123)

    Extra arguments can be passed to individual logging calls, and will
    take priority over any set with the set_extra_args call. Also a
    prefix can be specified using a subclass that will be put in front
    of the extra argument names for individual calls when storing them:

    >>> class PFXLogger(ExtraLogger):
    >>>     prefix = 'pfx.'

    """

    extra_args = {}
    prefix = ''

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        extra_args = self.extra_args

        # per thread extras
        class _perthread_extra(threading.local):
            def __init__(self):
                self.args = extra_args.copy()
        self._extra = _perthread_extra()

    def add_extra_args(self, extra_args):
        """Attach 'extra' arguments you want to be passed to every log message
           on the current thread.

        :param extra_args: A mapping type that contains the extra arguments you
            want to add.
        :raises TypeError: if extra_args is not a mapping type.

        """
        if not isinstance(extra_args, collections.Mapping):
            raise TypeError("extra_args must be a mapping")
        self._extra.args.update(extra_args)

    def reset_extra_args(self):
        """Reset all 'extra' arguments to every log message attached
           on the current thread.
        """
        self._extra.args = self.extra_args.copy()

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, user_extra=None, sinfo=None):
        extra = self._extra.args.copy()
        if user_extra:
            for k, v in user_extra.items():
                extra[self.prefix + k] = v
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info,
                                  func, extra, sinfo)
