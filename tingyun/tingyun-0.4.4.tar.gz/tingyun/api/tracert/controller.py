"""this module used to implements the api for control the agent's actions include data collect and upload

"""

import atexit
import sys
import os
import time
import logging
import threading
import traceback
from tingyun.api.log_file import initialize_logging
import tingyun.api.settings
import tingyun.api.tracert.application
from tingyun.api.platform import six
from tingyun.api.mapper import CONSTANCE_OUT_DATE_CONFIG, CONSTANCE_INVALID_DATA_TOKEN


_logger = logging.getLogger(__name__)


class Controller(object):
    """it is a agent core function center, include control function about the agent
    """
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self, config):
        """
        """
        _logger.info("Start python agent with version %s", config.agent_version)

        self._last_harvest = 0.0
        # used to record the application connect status. avoid more connection thread to server .
        self._connect_status = {}

        self._harvest_thread = threading.Thread(target=self._harvest_loop, name="TingYun-Harvest-Thread")
        self._harvest_thread.setDaemon(True)  # should take caution to the doc
        self._harvest_shutdown = threading.Event()

        self._config = config
        self._lock = threading.Lock()
        self._process_shutdown = False
        self._applications = {}  # used to store the actived applications
        self.__max_transaction = 5000

        if self._config.enabled:
            atexit.register(self._atexit_shutdown)

            # bind our exit event to the uwsgi shutdown event to facilitate the graceful reload of workers
            # should read more more information from uwsgi documentation
            if 'uwsgi' in sys.modules:
                import uwsgi
                uwsgi_original_atexit_callback = getattr(uwsgi, 'atexit', None)

                def uwsgi_atexit_callback():
                    self._atexit_shutdown()
                    if uwsgi_original_atexit_callback:
                        uwsgi_original_atexit_callback()

                uwsgi.atexit = uwsgi_atexit_callback

    @staticmethod
    def singleton_instance():
        """
        :return: singleton instance
        """
        if Controller._instance:
            return Controller._instance

        setting = tingyun.api.settings.global_settings()
        initialize_logging(setting.log_file, setting.log_level)

        instance = None
        with Controller._instance_lock:
            if not Controller._instance:
                instance = Controller(setting)
                Controller._instance = instance
                
                _logger.info('Creating instance of agent controller in  process %d.', os.getpid())
                _logger.info('Agent controller was initialized from: %r', ''.join(traceback.format_stack()[:-1]))
                 
        if instance:
            instance.active_controller()
            
        return instance

    def global_settings(self):
        """
        :return:
        """
        return tingyun.api.settings.global_settings()

    def application_settings(self, app_name):
        """
        :param app_name:
        :return:
        """
        application = self._applications.get(app_name, None)
        if application:
            return application.application_config

    def _harvest_loop(self):
        """the real metric data harvest thread
        :rtype : None
        """
        _logger.info("start harvest thread with id %s", os.getpid())

        self.__next_harvest = time.time()
        last_harvest = time.time()
        try:
            while 1:
                # it's not a bug, just for deal the special situation
                if self._harvest_shutdown.isSet():  # python2.6 earlier api
                    self._do_harvest(last_harvest, time.time(), shutdown=True)
                    _logger.info("exit the controller first loop.")
                    return

                # we are not going to report in 1 min strictly, because the application or data maybe too large,
                # so extend the time appropriately according to the last report situation
                now = time.time()
                while self.__next_harvest <= now:
                    self.__next_harvest += 60.0

                self._harvest_shutdown.wait(self.__next_harvest - now)

                if self._harvest_shutdown.isSet():  # force do last harvest
                    self._do_harvest(last_harvest, time.time())
                    _logger.info("exit controller harvest loop at shutdown signal with last harvest.")
                    return

                self._do_harvest(last_harvest, time.time())
                last_harvest = time.time()
        except Exception as err:
            _logger.warning("error occurred %s", err)
            if self._process_shutdown:  # python interpreter exit
                _logger.critical('''Unexpected exception in main harvest loop when process being shutdown. This can occur
                                 in rare cases due to the main thread cleaning up and destroying objects while the
                                 background harvest thread is still running. If this message occurs rarely,
                                 it can be ignored. If the message occurs on a regular basis,
                                 then please report it to Ting Yun support for further investigation.''')
            else:                       # other error.
                _logger.critical('''Unexpected exception in main harvest loop. Please report this problem to Ting Yun
                                support for further investigation''')

    def _do_harvest(self, last_harvest, current_harvest, shutdown=False):
        """do the really harvest action
        :param shutdown: sign the agent status, shutdown or not
        :return:
        """
        self._last_harvest = time.time()

        for name, application in six.iteritems(self._applications):

            try:
                _logger.debug("Harvest data for application %s", name)
                ret = application.harvest(last_harvest, current_harvest, shutdown)
                if ret and (CONSTANCE_OUT_DATE_CONFIG == ret[0] or CONSTANCE_INVALID_DATA_TOKEN == ret[0]):
                    application.stop_connecting()
                    application.activate_session()
            except Exception as err:
                _logger.exception("Errors occurred when harvest application %s, %s", name, err)

        _logger.info("Spend %.2fs to harvest all applications.", time.time() - self._last_harvest)

    def active_controller(self):
        """active a background controller thread if agent is enabled in settings
        """
        _logger.info('Start Agent controller main thread in process %s', os.getpid())
        if not self._config.enabled:
            _logger.info("agent is disabled,  agent controller not started.")
            return

        try:
            if self._harvest_thread.isAlive():
                _logger.info("agent controller was started, skip active it now.")
            else:
                _logger.info("Starting harvest thread now...")
                self._harvest_thread.start()

        except Exception as err:
            self._process_shutdown = True
            self.shutdown_controller()
            _logger.fatal("This exception indicates maybe internal agent python code error. please report to us"
                          " for further investigation. thank u.")
            _logger.fatal("Agent will stop work in this thread %s, %s", os.getpid(), err)

    def active_application(self, app_name, link_app=""):
        """active the core application for collecting or report
        :param app_name: the application name. Note, current stage only one application supported
        :param link_app: the application linked application
        :return: None
        """
        # this should be local settings
        if not self._config.enabled:
            _logger.info("Agent was disabled in configure file.")
            return

        # the connection thread is working(always), so skip it
        if app_name in self._connect_status:
            return

        active_app = None
        with self._lock:
            app = self._applications.get(app_name, None)
            if not app:
                app = tingyun.api.tracert.application.Application(app_name, link_app)
                self._applications[app_name] = app
                self._connect_status[app_name] = True
                active_app = True

        if active_app:
            app.activate_session()

    def _atexit_shutdown(self):
        """define for python interpreter exit event
        :return:
        """

        self._process_shutdown = True
        self.shutdown_controller()

    def shutdown_controller(self, timeout=None):
        """shutdown the controller through the event signal
        """
        if timeout is None:
            timeout = self._config.shutdown_timeout

        if not self._harvest_shutdown.isSet():
            return

        # stop the connecting thread, if has.
        for name, application in six.iteritems(self._applications):
            application.stop_connecting()

        self._harvest_shutdown.set()
        self._harvest_thread.join(timeout)

        _logger.info('Tingyun agent is Shutdown...')
        
    def record_transaction(self, app_name, transaction_node):
        """
        """
        application = self._applications.get(app_name, None)
        if application is None:
            _logger.warning("Application %s not exist, if this is not expected, please contact us for help.", app_name)
            return

        # server disabled or agent not registered, skip to record the transaction data
        if not application.active:
            _logger.debug("Agent not registered to agent server, skip to record transaction data.")
            return

        if not application.application_config.enabled:
            _logger.debug("Agent disabled by server side, skip to record transaction data.")
            return

        application.record_transaction(transaction_node)


def controller_instance():
    """
    :return: the singleton controller object
    """
    return Controller.singleton_instance()
