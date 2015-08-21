import logging
from optparse import make_option
import sys
from contextlib import contextmanager
from okscraper_django.models import ScraperRun, ScraperRunLog
import traceback
from django.core.management.base import NoArgsCommand, BaseCommand
from django.utils import timezone


class DbLogHandler(logging.Handler):

    def __init__(self, command):
        self.command = command
        super(DbLogHandler, self).__init__()

    def emit(self, record):
        self.command.db_log_handler_emit(record.levelname, record.getMessage())


class CommandDbLogMixin(object):
    def __init__(self):
        self.option_list = self.option_list + (
            make_option('--no-dblog', action='store_true', dest='nodblog', help="don't log run details to db"),
        )
        self._db_log_debug_msgs = []

    def _log_error(self, msg):
        self._logger.error(msg)

    def _log_warn(self, msg):
        self._logger.warning(msg)

    def _log_info(self, msg):
        self._logger.info(msg)

    def _log_debug(self, msg):
        self._logger.debug(msg)

    def _get_logger_name(self):
        base_name = getattr(self, 'BASE_LOGGER_NAME', '')
        if base_name != '':
            base_name += '.'
        return base_name + self._get_scraper_label()

    def _get_scraper_label(self):
        if len(sys.argv) > 1:
            return sys.argv[1]
        else:
            return __name__

    def _get_log_level_from_verbosity(self, verbosity):
        return {
            '1': logging.WARN,
            '2': logging.INFO,
            '3': logging.DEBUG
        }.get(str(verbosity), logging.ERROR)

    def _get_print_log_handler(self, log_level):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        return handler

    def _get_db_log_handler(self):
        handler = DbLogHandler(self)
        handler.setLevel(logging.DEBUG)
        return handler

    def _initialize_logger(self, print_verbosity, dblog):
        self._logger = logging.getLogger(self._get_logger_name())
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._get_print_log_handler(self._get_log_level_from_verbosity(print_verbosity)))
        if dblog:
            self._logger.addHandler(self._get_db_log_handler())
        self._log_debug('Initialized logger (print_verbosity=%s, dblog=%s)'%(print_verbosity, dblog))

    def _db_log_pre_handle(self, options):
        self._initialize_logger(options.get('verbosity'), options.get('dblog'))

    @contextmanager
    def _db_log_handle(self, options):
        self._dblog = not options.get('nodblog')
        self._initialize_logger(options.get('verbosity'), self._dblog)
        if self._dblog:
            self._scraper_run = ScraperRun(scraper_label=self._get_scraper_label())
            self._scraper_run.save()
        try:
            yield
        except:
            self.db_log_handler_emit('ERROR', traceback.format_exc())
            raise

    def db_log_handler_emit(self, log_level, msg):
        if self._dblog and hasattr(self, '_scraper_run'):
            if log_level == 'DEBUG':
                self._db_log_debug_msgs.append((timezone.now(), msg))
            else:
                if log_level == 'ERROR':
                    for debuglogtime, debuglogmsg in self._db_log_debug_msgs:
                        runlog = ScraperRunLog.objects.create(status='DEBUG', text=debuglogmsg, time=debuglogtime)
                        self._scraper_run.logs.add(runlog)
                    self._db_log_debug_msgs = []
                self._scraper_run.logs.add(ScraperRunLog.objects.create(status=log_level, text=msg))


class BaseDbLogCommand(BaseCommand, CommandDbLogMixin):

    def __init__(self):
        BaseCommand.__init__(self)
        CommandDbLogMixin.__init__(self)

    def handle(self, *args, **options):
        with self._db_log_handle(options):
            self._handle(*args, **options)

    def _handle(self, *args, **options):
        raise Exception()


class NoArgsDbLogCommand(NoArgsCommand, CommandDbLogMixin):

    def __init__(self):
        NoArgsCommand.__init__(self)
        CommandDbLogMixin.__init__(self)

    def handle_noargs(self, **options):
        with self._db_log_handle(options):
            self._handle_noargs(**options)

    def _handle_noargs(self, **options):
        raise Exception()
