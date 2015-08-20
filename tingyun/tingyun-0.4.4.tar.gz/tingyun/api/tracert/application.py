"""This module implements data recording and reporting for an application

"""

import logging
import threading
import time
import sys

from tingyun.api.tracert.uploader import create_session
from tingyun.api.settings import global_settings
from tingyun.api.tracert.environment import env_config
from tingyun.api.tracert.data_engine import DataEngine
from tingyun.api.tracert.profile import get_profile_manger
from tingyun.api.exception import InvalidLicenseException, OutOfDateConfigException, InvalidDataTokenException
from tingyun.api.exception import RetryDataForRequest, DiscardDataForRequest, ServerIsUnavailable

from tingyun.api.mapper import CONSTANCE_OUT_DATE_CONFIG, CONSTANCE_RETRY_DATA, CONSTANCE_SERVER_UNAVAILABLE
from tingyun.api.mapper import CONSTANCE_DISCARD_DATA, CONSTANCE_HARVEST_ERROR, CONSTANCE_INVALID_DATA_TOKEN
from tingyun.api.mapper import CONSTANCE_LICENSE_INVALID, CONSTANCE_SESSION_NOT_ACTIVED

_logger = logging.getLogger(__name__)


class Application(object):
    """Real web application property/action/control holder/controller
    """
    def __init__(self, app_name, linked_app=[]):
        """
        :param app_name: a real python/project application name, usually write in config file
        :param linked_app: linked app name for app
        :return:
        """
        _logger.debug("Init Application with name %s, linked-name %s", app_name, linked_app)

        self._app_name = app_name
        self._linked_app = sorted(set(linked_app))
        self._active_session = None
        self._is_license_valid = True

        self.connect_retry_time = 30
        self._connect_event = threading.Event()
        self._stats_lock = threading.Lock()  # used to lock the core collect data
        self._data_engine = DataEngine()

        self._agent_commands_lock = threading.Lock()
        self.profile_manager = get_profile_manger()
        self.profile_status = False

        self.__max_transaction = 2000
        self._transaction_count = 0
        self._last_transaction = 0.0
        self.metric_name_ids = {"actions": {}, "apdex": {}, "components": {}, "general": {}, "errors": {}}

    @property
    def active(self):
        """
        :return:
        """
        return self._active_session is not None

    @property
    def application_config(self):
        """return the configuration of the application, it's downloaded from server witch is merged with uploaded
        settings with server config on server
        :return:
        """
        return self._active_session and self._active_session.config

    def stop_connecting(self):
        """
        :return:
        """
        self._connect_event.set()

    def shutdown_internal_service(self):
        """used to shutdown the internal commands service.
        :return:
        """
        self.profile_manager.shutdown()

    def activate_session(self):
        """active a session(background thread) to register the application
        :return:
        """
        # TODO: do some check for agent status
        self._connect_event.clear()

        connect_thread = threading.Thread(target=self.connect_to_data_server,
                                          name="TingYun-session-thread-%s" % int(time.time()))
        connect_thread.setDaemon(True)
        connect_thread.start()

        return True

    def connect_to_data_server(self):
        """Performs the actual registration of the application to server, get server config and set the current app
        settings.
        :return:
        """
        # TODO: do some check for agent status
        if self._active_session:
            _logger.info("Application is actived, skip to connect to server.")
            return True

        # ensure the main thread get to run first
        time.sleep(0.01)

        while not self._active_session:
            settings = global_settings()
            try:
                active_session = create_session(None, self._app_name, self._linked_app, env_config(), settings)
            except InvalidLicenseException as _:
                self._is_license_valid = False
                _logger.warning("Invalid license in configuration, agent will stop to work please fix license and"
                                "restart agent again")
                break
            except Exception as _:
                # use the harvest controller signal to control the connection
                _logger.exception("Connect to agent server failed, Connection will try again in 1 min.")
                self._connect_event.wait(self.connect_retry_time)
                if self._connect_event.isSet():
                    _logger.info("Agent is shutting down, stop the connection to server now.")
                    return

                continue

            if active_session:
                self._is_license_valid = True
                self._connect_event.set()

                # set the application settings to data engine
                with self._stats_lock:
                    self._active_session = active_session
                    self._data_engine.reset_stats(self._active_session.config)

    def harvest(self, last_harvest, current_harvest, shutdown=False):
        """Performs a harvest, reporting aggregated data for the current reporting period to the server.
        :return:
        """
        ret_code = 0

        # controller should ignore session/license error code, because the connecting thread doing/did it
        if not self._active_session:
            _logger.info("Application not registered to server yet, skip harvest data.")
            return CONSTANCE_SESSION_NOT_ACTIVED, self._app_name, self._linked_app

        if not self._is_license_valid:
            _logger.debug("The license is invalid, skip harvest data.")
            return CONSTANCE_LICENSE_INVALID, self._app_name, self._linked_app

        with self._stats_lock:
            self._transaction_count = 0
            self._last_transaction = 0.0
            stat = self._data_engine.stats_snapshot()

        try:
            config = self.application_config

            # send metric data
            performance_metric = self.get_performance_metric(stat, last_harvest, current_harvest, config.audit_mode)
            if config.audit_mode:
                _logger.info("Agent capture the performance data %s", performance_metric)

            result = self._active_session.send_performance_metric(performance_metric)
            self.process_metric_id(result, config.daemon_debug)

            if config.error_collector.enabled:
                error_trace = self.get_error_trace_data(stat)
                self._active_session.send_error_trace(error_trace)

                if config.audit_mode:
                    _logger.info("Agent capture the error trace data %s", error_trace)

            if config.action_tracer.enabled:
                slow_action_data = stat.action_trace_data()
                self._active_session.send_action_trace(slow_action_data)

                if config.audit_mode:
                    _logger.info("Agent capture the slow action data %s", slow_action_data)

            if config.action_tracer.slow_sql:
                slow_sql_data = stat.slow_sql_data()
                self._active_session.send_sql_trace(slow_sql_data)

                if config.audit_mode:
                    _logger.info("Agent capture the slow sql data %s", slow_sql_data)

            stat.reset_metric_stats()

            # get the commands and execute it.
            self.process_agent_command()
            self.send_profile_data(config.audit_mode)

            if shutdown:
                self.shutdown_internal_service()
        except OutOfDateConfigException as _:
            # need to reset the connection
            self._active_session = None
            ret_code = CONSTANCE_OUT_DATE_CONFIG
            _logger.info("Config changed in server, reset the connect now.")
        except InvalidDataTokenException as _:
            # need to reset the connection
            self._active_session = None
            ret_code = CONSTANCE_INVALID_DATA_TOKEN
            _logger.info("Data token is valid, register the application %s again now", self._app_name)
        except DiscardDataForRequest as _:
            ret_code = CONSTANCE_DISCARD_DATA
        except ServerIsUnavailable as _:
            ret_code = CONSTANCE_SERVER_UNAVAILABLE
        except RetryDataForRequest as _:
            ret_code = CONSTANCE_RETRY_DATA

            with self._stats_lock:
                try:
                    self._data_engine.rollback(stat)
                except Exception as err:
                    _logger.warning("rollback performance data failed. %s", err)

            _logger.debug("This exception indicates server service can not touched. if this error continues. please "
                          "report to us for further investigation. thank u")
        except Exception as err:
            ret_code = CONSTANCE_HARVEST_ERROR
            _logger.exception("This exception indicates maybe internal agent code error. if this error continues. "
                              "please report to us for further investigation. thank u.")
            _logger.exception("%s", err)

        return ret_code, self._app_name, self._linked_app
        
    def record_transaction(self, transaction):
        """
        """
        if not self._active_session or not self._data_engine.settings:
            _logger.debug("Agent server is disconnected, transaction data will be dropped.")
            return False

        try:
            stat = self._data_engine.create_data_zone()
            stat.record_transaction(transaction)

            self._transaction_count += 1
            self._last_transaction = transaction.end_time

            with self._stats_lock:
                self._data_engine.merge_metric_stats(stat)
        except Exception as err:
            _logger.exception("Unexpected error occurred when record transaction to stat, that's maybe internal "
                              "implement issue, if this continues, please report to us for further investigation."
                              "%s", err)

        return False

    def process_metric_id(self, metric_ids, debug_mode=False):
        """keep the metric id in the memory for replace the key
        :param metric_ids:the metric ids download from server.
        :return:
        """
        if not metric_ids or debug_mode:
            return self.metric_name_ids

        if "actions" in metric_ids:
            for item in metric_ids["actions"]:
                key = item[0]["name"].encode("utf8")
                self.metric_name_ids["actions"][key] = item[1]

        if "apdex" in metric_ids:
            for item in metric_ids["apdex"]:
                key = item[0]["name"].encode("utf8")
                self.metric_name_ids["apdex"][key] = item[1]

        if "general" in metric_ids:
            for item in metric_ids["general"]:
                key = item[0]["name"].encode("utf8")
                self.metric_name_ids["general"][key] = item[1]

        if "errors" in metric_ids:
            for item in metric_ids["errors"]:
                key = item[0]["name"].encode("utf8")
                self.metric_name_ids["errors"][key] = item[1]

        if "components" in metric_ids:
            for item in metric_ids["components"]:
                key = "%s:%s" % (item[0]["name"], item[0]["parent"])
                key = key.encode("utf8")
                self.metric_name_ids["components"][key] = item[1]

        return self.metric_name_ids

    def get_performance_metric(self, stat, last_harvest, current_harvest, audit_mode=False):
        """
        :param stat:
        :return:
        """
        # disable the id mechanism
        metric_name_ids = self.metric_name_ids
        if audit_mode:
            metric_name_ids = {"actions": {}, "apdex": {}, "components": {}, "general": {}, "errors": {}}

        performance = {
            "type": "perfMetrics",
            "timeFrom": int(last_harvest),
            "timeTo": int(current_harvest),
            "interval": int(current_harvest - last_harvest),
            "actions": stat.action_metrics(metric_name_ids["actions"]),
            "apdex": stat.apdex_data(metric_name_ids["apdex"]),
            "components": stat.component_metrics(metric_name_ids["components"]),
            "general": stat.general_trace_metric(metric_name_ids["general"]),
            "errors": stat.error_stats(metric_name_ids["errors"]),
        }

        return performance

    def get_error_trace_data(self, stat):
        """
        :return:
        """
        error_trace = {
            "type": "errorTraceData",
            "errors": stat.error_trace_data()
        }

        # no error data recorded return None as mark.
        if 0 == len(stat.error_trace_data()):
            error_trace = []

        return error_trace

    def process_agent_command(self):
        """get the command from agent server, and start the command.
        :return:
        """
        # use the lock for only sure one processes on the agent command

        with self._agent_commands_lock:
            for cmd in self._active_session.request_agent_commands():
                _logger.info("Processing command %s", cmd)

                cmd_id = None
                if 'StopProfiler' not in cmd['name']:
                    cmd_id = cmd['id']

                cmd_name = cmd['name']
                cmd_args = cmd['args']

                cmd_handler = getattr(self, "cmd_%s" % cmd_name, None)
                if cmd_handler is None:
                    _logger.info("Agent dose not support command %s", cmd_name)
                    continue

                cmd_handler(cmd_id, cmd_args)

    def cmd_StartProfiler(self, cid, args):
        """start profile function, we define this just for adapt to auto match the commands
        :param cid: command id
        :param args: command args
        :return: None
        """
        profile_id = args["profileId"]
        duration = args['duration']
        interval = args['interval']

        if self.profile_status:
            return

        if not hasattr(sys, "_current_frames"):
            """
            """
            _logger.warning("The current Python interpreter being used is not support thread profiling. For help about"
                            "additional information about the thread profiling, please contact our support.")
            return

        self.profile_status = self.profile_manager.start_profile(cid, self._app_name, profile_id, duration, interval)
        if not self.profile_status:
            _logger.warning("profiler is running now, so skip current profile command. %s", args)
            return

        _logger.info("Starting thread profile for application %s, with duration %ss,  interval %sms",
                     self._app_name, duration, interval)

    def cmd_StopProfiler(self, cid, args):
        """ stop the profile commands
        """
        profile_id = args['profileId']
        profile = self.profile_manager.current_profile
        cmd_id = self.profile_manager.cmd_info['cid']

        if profile is None:
            _logger.warning("Get stop profile commands, but threading profiling is not running. if this continues, "
                            "please report to us for more investigation.")
        elif profile_id != profile.profile_id:
            self._active_session.send_profile_data({"id": cmd_id, "result": {}})
            _logger.warning("Get stop profile commands, but the specified profile id[%s] not match current"
                            "profile id[%s]. This command will be ignored.", profile_id, profile.profile_id)
            return

        self.profile_manager.shutdown(stop_cmd=True)
        self._active_session.send_profile_data({"id": cmd_id, "result": {}})
        self.profile_status = None
        _logger.info("Stopping profile for application %s", self._app_name)

    def send_profile_data(self, audit_mode=False):
        """get the profile data and send the agent server
        :return:
        """
        # profile thread start failed. skip report process
        if not self.profile_status:
            return

        profile_data = self.profile_manager.generate_profile_data()

        # dose not finished.
        if profile_data is None:
            return

        if audit_mode:
            _logger.info("Agent capture the profile data %s", profile_data)

        ret = self._active_session.send_profile_data(profile_data)
        self.profile_status = None
        _logger.info("send profile return result %s", ret)