"""this module implement the connection and data uploader to server

"""
import json
import logging
import socket
import time
import sys
import zlib

import tingyun.api.requests as requests
from tingyun.api.platform import six
from tingyun.api.settings import global_settings, merge_settings, get_upload_settings
from tingyun.api.exception import DiscardDataForRequest, RetryDataForRequest, InvalidLicenseException
from tingyun.api.exception import InvalidDataTokenException, OutOfDateConfigException, ServerIsUnavailable

_logger = logging.getLogger(__name__)
USER_AGENT = ' NBS Newlens Agent/%s (python %s; %s)' % (global_settings().agent_version, sys.version.split()[0],
                                                        sys.platform)


class ApplicationSession(object):
    """this class hold the application session information from server
    """

    def __init__(self, url, config, license_key, redirect_host):
        self.url = url
        self.config = config
        self.license_key = license_key
        self.local_setting = global_settings()
        self.merged_settings = config
        self.redirect_host = redirect_host

        self._session = None
        self.request_param = {
            "licenseKey": self.license_key,
            "version": self.local_setting.data_version,
            "appSessionKey": self.config.appSessionKey,
        }

    @property
    def session(self):
        """
        :return:
        """
        if self._session is None:
            self._session = requests.session()

        return self._session

    def close_session(self):
        """use to shutdown session, report status to server for test.
        """
        self._session.close()
        self._session = None

    def send_performance_metric(self, metric_data):
        """
        """
        return send_request(self.session, self.url, "send_collect_data", metric_data, self.request_param,
                            self.config.audit_mode)

    def send_error_trace(self, error_trace):
        """
        """
        if not error_trace:
            return

        return send_request(self.session, self.url, "send_error_trace", error_trace, self.request_param,
                            self.config.audit_mode)

    def send_action_trace(self, action_trace):
        """
        """
        if not action_trace:
            return

        return send_request(self.session, self.url, "send_action_trace", action_trace, self.request_param,
                            self.config.audit_mode)

    def send_sql_trace(self, sql_trace):
        """
        """
        if not sql_trace:
            return

        return send_request(self.session, self.url, "send_sql_trace", sql_trace, self.request_param,
                            self.config.audit_mode)

    def send_profile_data(self, data):
        """it allow to send empty data.
        """
        audit_mode = self.config.audit_mode
        url = connect_url("uploadAgentCommands", self.redirect_host)
        return send_request(self.session, url, "send_profile_data", data, self.request_param, audit_mode)

    def request_agent_commands(self):
        """
        """
        url = connect_url("getAgentCommands", self.redirect_host)
        audit_mode = self.config.audit_mode
        result = send_request(self.session, url, "get_agent_commands", {}, self.request_param, audit_mode)

        return result


def connect_url(action, host=None):
    """
    :param action: the uploader actually intention
    :return: ruled url, the suitable url according to server
    """
    settings = global_settings()
    scheme = settings.ssl and 'https' or 'http'
    url = "%s://%s/%s"

    if host is None:
        host = settings.host

    return url % (scheme, host, action)


def create_session(license_key, app_name, linked_applications, machine_env, settings):
    """
    :return:
    """
    start_time = time.time()

    if not license_key:
        license_key = settings.license_key

    if not license_key:
        _logger.error("license key should be provided in tingyun.ini config file, agent may can not started.")

    try:
        _logger.info("create session with license: %s, app: %s, link app: %s, env: %s, settings: %s",
                     license_key, app_name, linked_applications, machine_env, settings)

        url = connect_url("getRedirectHost")
        param = {"licenseKey": license_key, "version": settings.data_version}
        redirect_host = send_request(None, url, "getRedirectHost", {}, param)
        local_conf = {
            "host": socket.gethostname(),
            "appName": [app_name] + linked_applications,
            "language": "Python",
            "agentVersion": settings.agent_version,
            "config": get_upload_settings(),
            "env": machine_env
        }

        url = connect_url("initAgentApp", redirect_host)
        server_conf = send_request(None, url, "initAgentApp", local_conf, {"licenseKey": license_key})
        app_config = merge_settings(server_conf)
    except Exception as err:
        _logger.error("errors when connect to server %s", err)
        raise RetryDataForRequest("Errors occurred, when create session with server. %s" % err)
    else:
        _logger.info("Successful register application to agent server with name: %s, use time: %ss", app_name,
                     time.time() - start_time)

        url = connect_url("upload", redirect_host)
        return ApplicationSession(url, app_config, license_key, redirect_host)


def send_request(session, url, action, payload={}, param={}, audit_mode=False):
    """
    :param session: the request session to server
    :param url: the address witch data send to
    :param action: the send actually intention
    :param payload: request data
    :return: None
    """
    _logger.debug("Send request with url %s, action %s param %s", url, action, param)
    settings = global_settings()
    start_time = time.time()
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/octet-stream",
        "connection": "close",
        "Accept-Encoding": "deflate",
    }

    try:
        data = json.dumps(payload)
    except Exception as err:
        _logger.error("Encoding json for payload failed, url %s action %s param %s payload %s err %s",
                      url, action, param, payload, err)
        raise DiscardDataForRequest(str(sys.exc_info()[1]))

    # compress if data length more than 10kbi
    if len(data) > 10 * 1024:
        headers['Content-Encoding'] = 'deflate'
        level = (len(data) < 2000000) and 1 or 9
        data = zlib.compress(six.b(data), level)

    auto_close_session = False
    if not session:
        session = requests.session()
        auto_close_session = True

    content = ""
    try:
        timeout = settings.data_report_timeout
        ret = session.post(url, data=data, params=param, headers=headers, timeout=timeout)
        content = ret.content
    except requests.RequestException:
        _logger.error('Agent server is not attachable. if the error continues, please report to networkbench.'
                      'The error raised was %r.', sys.exc_info()[1])
        _logger.warning("Response content is %s", content)
        raise RetryDataForRequest(str(sys.exc_info()[1]))
    finally:
        duration = time.time() - start_time
        if auto_close_session:
            session.close()

    if audit_mode:
        _logger.info("Use %ss to upload data return value %r", duration, content)

    if ret.status_code == 400:
        _logger.error("Bad request has been submitted for url %s, please report this to us, thank u.", url)
        raise DiscardDataForRequest()
    elif ret.status_code == 503:
        _logger.error("Agent server is unavailable. This can be a transient issue because of the server or our core"
                      " application being restarted. if this error continues, please report to us. thank u.")
        raise DiscardDataForRequest()
    elif ret.status_code == 502:
        _logger.error("Agent server error, our engineer has caution this error, thanks for your support")
        raise ServerIsUnavailable("service unavailable, get status code 502")
    elif ret.status_code != 200:
        _logger.warning("We got none 200 status code %s, this maybe some network/server error, if this error continues,"
                        "please report to us . thanks for your support. return content %s", ret.status_code, ret)
        raise DiscardDataForRequest()

    try:
        if six.PY3:
            content = content.decode('UTF-8')

        result = json.loads(content)
    except Exception as err:
        _logger.warning("Decoding data for Json error. please contact us for further investigation. %s", err)
        raise DiscardDataForRequest(str(sys.exc_info()[1]))
    else:
        # successful exchange with server
        if result["status"] == "success":
            return result["result"] if "result" in result else []

    _logger.info("get unexpected return,  there maybe some issue. %s", result)
    server_status = int(result["result"]["errorCode"])

    if server_status == 460:
        _logger.warning("Invalid license key, Please contact to networkbench for more help.")
        raise InvalidLicenseException("Invalid license key")
    elif server_status == 462:
        _logger.warning("Invalid data format, maybe something get wrong when json encoding.")
        raise DiscardDataForRequest(content)
    elif server_status == 461:
        _logger.warning("Invalid data token, if this error continues, please report to networkbench support for further"
                        " investigation")
        raise InvalidDataTokenException()
    elif server_status == -1:
        _logger.warning("Agent server error, our engineer has caution this error, thanks for your support.")
        raise ServerIsUnavailable()
    elif server_status == 470:
        _logger.info("Configuration is out of date, server configuration will be obtain again")
        raise OutOfDateConfigException()

    return []
