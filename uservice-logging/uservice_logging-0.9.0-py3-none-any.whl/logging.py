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
import logging
import logging.handlers
import logstash
import os
import socket

__all__ = [
    'configure_service_logging'
]

_logging_configured = []


def configure_logging(config, service, **kwds):
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
    return configure_service_logging(log_path, logstash_config)


def configure_service_logging(log_file_path=None, logstash_config=None):
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

    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Silence requests logging, which is created by nova, keystone and swift.
    requests_logger = logging.getLogger('requests')
    requests_logger.setLevel(logging.WARNING)

    # If there is no .directory for the file, fall back to stderr logging
    if log_file_path and os.path.exists(os.path.dirname(log_file_path)):
        handler = logging.handlers.TimedRotatingFileHandler(
            log_file_path,
            when='D',
            interval=1
        )
    else:
        print("parent directory for log '{}' does not exist, using stderr "
              "for app log.".format(log_file_path))
        handler = logging.StreamHandler()

    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s  %(name)s %(levelname)s: %(message)s'
        )
    )
    root_logger.addHandler(handler)

    if logstash_config:
        root_logger.addHandler(
            logstash.LogstashHandler(
                logstash_config['host'],
                int(logstash_config['port']),
                version=int(logstash_config['version'])
            )
        )


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

    def set_extra_args(self, extra_args):
        """Set the 'extra' arguments you want to be passed to every log message.

        :param extra_args: A mapping type that contains the extra arguments you
            want to store.
        :raises TypeError: if extra_args is not a mapping type.

        """
        if not isinstance(extra_args, collections.Mapping):
            raise TypeError("extra_args must be a mapping")
        self.extra_args = extra_args

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, user_extra=None, sinfo=None):
        extra = self.extra_args.copy()
        if user_extra:
            for k, v in user_extra.items():
                extra[self.prefix + k] = v
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info,
                                  func, extra, sinfo)
