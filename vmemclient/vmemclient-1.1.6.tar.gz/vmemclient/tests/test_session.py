"""
Copyright 2015 Violin Memory, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import json
import os
import sys
import unittest
import urllib2

import mock

import vmemclient
import vmemclient.core.session
import vmemclient.core.request

from vmemclient.core.error import *


# Constants
SESSION_HOST = 'my-host.int'
SESSION_USERNAME = 'admin'
SESSION_PASSWORD = 'admin'
SESSION_DEBUG = False
SESSION_PROTOCOL = 'https'
SESSION_KEEPALIVE = False
SESSION_LOG_FD = None
SESSION_PORT = None

GENERIC_SUCCESS = {
    'success': True,
    'msg': 'Success',
}
GENERIC_SUCCESS_AS_JSON_STRING = json.dumps(GENERIC_SUCCESS)

INVALID_PATH_RESPONSE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>IPStor REST API Error Message </title>
</head>
<body>
  <h1>IPStor REST API Return Error</h1>
  <h2>An unexpected error has occurred</h2>

  
  <h3>Exception information:
  Page not found  </h3>
  <p>
      <b>Message:</b>  
      <FONT COLOR =#FF0000>  
      Invalid controller specified (foo) 
      </FONT> 
  </p>
 <h3>Stack trace:</h3>
  <pre>#0 /usr/local/zendframework/Zend/Controller/Front.php(954): Zend_Controller_Dispatcher_Standard->dispatch(Object(Zend_Controller_Request_Http), Object(Zend_Controller_Response_Http))
#1 /usr/local/zendframework/Zend/Application/Bootstrap/Bootstrap.php(97): Zend_Controller_Front->dispatch()
#2 /usr/local/zendframework/Zend/Application.php(366): Zend_Application_Bootstrap_Bootstrap->run()
#3 /PRODUCT/concerto/api/web/public/index.php(36): Zend_Application->run()
#4 {main}  </pre>

  <h3>Request Parameters:</h3>
  <pre>array (
  'controller' => 'foo',
  'action' => 'get',
  'id' => 'bar',
  'module' => 'default',
)  </pre>
  
  
  
</body>
</html>
"""

LOGIN_DATA = {u'id': u'c7fffdda-47db-59cf-a15d-2c3e041755d7'}

PROPERTIES_DATA = {
    u'success': True,
    u'data': {
        u'capacity': u'44375602102272',
        u'hardware_model': u'SHB-3',
        u'hostname': u'lab-fil3494-mg-b',
        u'kernel_version': u'Linux 2.6.32-358.23.2.el6.x86_64 #1 SMP Wed Oct 16 11:16:45 PDT 2013 x86_64',
        u'manufacturer': u'Violin',
        u'memory': u'203065278464',
        u'network_interface': [
            u'eth0 - mtu 1500  inet 10.5.10.45  mac 0:90:fb:51:68:14 mask 255.255.240.0',
            u'eth0.10 - mtu 1500  inet 169.254.1.102  mac 0:90:fb:51:68:14 mask 255.255.0.0',
            u'eth0:0 - mtu 1500  inet 10.5.10.66  mac 0:90:fb:51:68:14 mask 255.255.240.0',
            u'eth1 - mtu 1500  inet 169.254.3.102  mac 0:90:fb:51:68:15 mask 255.255.255.0',
            u'sci0 - mtu 16324  inet 169.254.2.102  mac 6:1b:97:51:68:14 mask 255.255.255.0'],
        u'os_version': u'Red Hat Enterprise Linux Server release 6.4 (Santiago)',
        u'processor': u'Intel(R) Xeon(R) CPU E5-2450 v2 @ 2.50GHz 2499 MHz',
        u'server_version': u'Violin Memory Concerto Server v7.5.5 - (Build 8975)',
        u'slot_type': u'mg-b',
        u'swap': u'8591048704',
        u'system_serial_number': u'1F503B00317',
    },
}



class TestCommonSession(unittest.TestCase):
    CLASS_UNDER_TEST = vmemclient.core.session.BasicSession

    def setUp(self):
        super(TestCommonSession, self).setUp()
        self.con = self.create_session_object()

    def create_session_object(self, **kwargs):
        config = {
            'host': 'my-host.int',
            'user': 'admin',
            'password': 'admin',
            'debug': False,
            'proto': 'https',
            'keepalive': False,
            'log_fd': None,
            'port': None,
        }
        config.update(kwargs)

        return self.CLASS_UNDER_TEST(**config)

    def test_create_basic_session_http_no_port(self):
        session = self.create_session_object(proto='http')
        self.assertTrue(session)
        self.assertEqual('http', session.proto)

    def test_create_basic_session_http_with_int_port(self):
        port_number = 80
        session = self.create_session_object(port=port_number)
        self.assertTrue(session)
        self.assertEqual(port_number, session.port)

    def test_create_basic_session_http_with_string_port(self):
        port_number = '80'
        session = self.create_session_object(port=port_number)
        self.assertTrue(session)
        self.assertEqual(int(port_number), session.port)

    def test_create_basic_session_with_custom_logger(self):
        class MyFakeLogger(object):
            def __init__(self):
                pass
            def write(self, msg):
                pass
            def flush(self):
                pass

        fake_logger = MyFakeLogger()
        session = self.create_session_object(log_fd=fake_logger)
        self.assertTrue(session)
        self.assertEqual(fake_logger, session.log_fd)

    def test_create_basic_session_failed_invalid_protocol(self):
        self.assertRaises(
            ValueError,
            self.create_session_object, proto='foo')

    def test_create_basic_session_failed_invalid_port(self):
        self.assertRaises(
            ValueError,
            self.create_session_object, port='foo')

    def test_create_basic_session_failed_invalid_logger(self):
        self.assertRaises(
            ValueError,
            self.create_session_object, log_fd='foo')

    def test_delete(self):
        self.con.close = mock.Mock()
        self.con.__del__()
        self.con.close.assert_called_once_with()

    def test_delete_catches_exceptions(self):
        self.con.close = mock.Mock(side_effect=Exception)
        self.con.__del__()
        self.assertEqual(self.con.close.call_count, 1)

    def test_login_calls_open(self):
        self.con.open = mock.Mock(return_value=True)
        value = self.con.login()
        self.assertTrue(value)

    def test_closed_property(self):
        self.assertEqual(self.con._closed, self.con.closed)

    def test_log(self):
        self.con.log_fd.write = mock.Mock()
        self.con.log_fd.flush = mock.Mock()

        value = self.con.log('Test is a test')

        self.assertTrue(value is None)

class TestBasicSession(TestCommonSession):
    def test_create_basic_session_https_no_port(self):
        session = self.create_session_object()
        self.assertTrue(session)
        self.assertEqual(None, session.port)

    def test_open(self):
        self.assertRaises(NotImplementedError, self.con.open)

    def test_close(self):
        self.assertRaises(NotImplementedError, self.con.close)


class TestXGSession(TestCommonSession):
    CLASS_UNDER_TEST = vmemclient.core.session.XGSession

    def create_session_object(self, **kwargs):
        config = {'host': 'my-host.int', 'autologin': False}
        config.update(kwargs)

        return self.CLASS_UNDER_TEST(**config)

    @mock.patch.object(vmemclient.core.session.XGSession, 'open')
    def test_create_basic_session(self, mock_open):
        mock_open.return_value = True

        session = self.create_session_object(autologin=True)

        self.assertTrue(session)
        self.assertEqual('admin', session.user)
        self.assertEqual('', session.password)
        self.assertEqual(False, session.debug)
        self.assertEqual('https', session.proto)
        self.assertEqual(False, session.keepalive)
        self.assertEqual(None, session.port)

    @mock.patch.object(vmemclient.core.session.XGSession, 'open')
    def test_create_session_with_failed_autologin_raises_exception(
            self, mock_open):
        mock_open.return_value = False

        self.assertRaises(
            AuthenticationError,
            self.create_session_object, autologin=True)

    def test_open_with_classic_response(self):
        config = {
            'read.return_value': 'template=index\nHTTP-EQUIV="Refresh"'}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)

        response = self.con.open()

        self.assertTrue(response)

    def test_open(self):
        config = {
            'read.return_value': "template=dashboard\nHTTP-EQUIV='Refresh'"}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)

        response = self.con.open()

        self.assertTrue(response)

    def test_open_failed_login(self):
        config = {'read.return_value': 'this will fail'}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)

        response = self.con.open()

        self.assertFalse(response)

    def test_close(self):
        config = {
            'read.return_value': 'You have been successfully logged out.'}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)
        self.con._closed = False

        response = self.con.close()

        self.assertEqual(None, response)
        self.assertTrue(self.con.closed)

    def test_close_failure_catches_exceptions(self):
        self.con._handle.open = mock.Mock(
            side_effect=urllib2.URLError('error'))
        self.con._closed = False

        response = self.con.close()
        self.assertEqual(None, response)

    def test_close_multiple_invocations(self):
        config = {
            'read.return_value': 'You have been successfully logged out.'}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)
        self.con._closed = False

        response1 = self.con.close()
        response2 = self.con.close()

        self.assertEqual(None, response1)
        self.assertEqual(None, response2)
        self.assertTrue(self.con.closed)
        self.assertEqual(1, self.con._handle.open.call_count)

    def test_get_version_info(self):
        mock_type = 'V'
        mock_version = '6.3.0'
        return_value = {'/system/version/release': mock_type + mock_version}

        self.con.get_node_values = mock.Mock(return_value=return_value)

        response = self.con._get_version_info()

        self.assertTrue('type' in response)
        self.assertEqual(mock_type, response['type'])
        self.assertTrue('version' in response)
        self.assertEqual(mock_version, response['version'])

    @mock.patch.object(vmemclient.core.response.XGResponse, 'fromstring')
    def test_send_request(self, mock_fromstring):
        expected = {}
        mock_fromstring.return_value = expected

        req = mock.Mock()
        req_config = {'to_xml.return_value': 'foo'}
        req.configure_mock(**req_config)

        resp_config = {'read.return_value': 'foo'}
        resp = mock.Mock()
        resp.configure_mock(**resp_config)
        self.con._handle.open = mock.Mock(return_value=resp)

        actual = self.con.send_request(req, None, True)

        self.assertEqual(expected, actual)

    def test_send_request_with_keepalive(self):
        self.con.keepalive = True

        req = mock.Mock()
        req_config = {'to_xml.return_value': 'foo'}
        req.configure_mock(**req_config)

        self.con.login = mock.Mock(return_value=True)

        self.con._handle.open = mock.Mock(side_effect=AuthenticationError)

        self.assertRaises(
            AuthenticationError,
            self.con.send_request, req, None, True)
        self.assertEqual(2, self.con._handle.open.call_count)
        self.assertTrue(self.con.closed)

    def test_send_request_raises_network_error(self):
        req = mock.Mock()
        req_config = {'to_xml.return_value': 'foo'}
        req.configure_mock(**req_config)

        self.con._handle.open = mock.Mock(
            side_effect=urllib2.URLError('error'))

        self.assertRaises(
            NetworkError,
            self.con.send_request, req, None, True)

    def test_save_config(self):
        expected = {'code': 0, 'message': None}

        self.con.perform_action = mock.Mock(return_value=expected)

        actual = self.con.save_config()

        self.assertEqual(expected, actual)

class TestConcertoSession(TestCommonSession):
    CLASS_UNDER_TEST = vmemclient.core.session.ConcertoJsonSession

    def create_session_object(self, **kwargs):
        config = {
            'host': 'my-host.int',
            'autologin': False,
            'port': 80,
        }
        config.update(kwargs)

        return self.CLASS_UNDER_TEST(**config)

    def test_open(self):
        config = {'read.return_value':
            '{"id":"da2286f2-f369-512c-bd87-3d81a02544b5"}'}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)
        self.con._reset_handle = mock.Mock()
        self.con.update_properties = mock.Mock()

        actual = self.con.open()

        self.assertTrue(actual)

    @mock.patch.object(vmemclient.core.session.JsonSession, 'open')
    def test_create_basic_session(self, mock_open):
        mock_open.return_value = True

        session = self.create_session_object(autologin=True)

        self.assertTrue(session)
        self.assertEqual('admin', session.user)
        self.assertEqual('', session.password)
        self.assertEqual(False, session.debug)
        self.assertEqual('http', session.proto)
        self.assertEqual(False, session.keepalive)
        self.assertEqual(80, session.port)

    @mock.patch.object(vmemclient.core.session.JsonSession, 'open')
    def test_create_session_with_failed_autologin_raises_exception(
            self, mock_open):
        mock_open.return_value = False

        self.assertRaises(
            AuthenticationError,
            self.create_session_object, autologin=True)

    def test_close_parent_function(self):
        self.con._close = mock.Mock()
        self.con._closed = False
        self.con.login_info = {'id': 'foo'}

        actual = self.con.close()

        self.assertTrue(actual is None)
        self.assertTrue(self.con._closed)
        self.assertTrue(self.con.login_info is None)

    def test_get(self):
        expected = GENERIC_SUCCESS
        location = '/some/location'
        self.con._communicate = mock.Mock(return_value=expected)

        actual = self.con.get(location)

        self.assertEqual(expected, actual)
        self.con._communicate.assert_called_once_with(
            vmemclient.core.request.GetRequest,
            location, None, None, None)

    def test_post(self):
        expected = GENERIC_SUCCESS
        location = '/some/location'
        self.con._communicate = mock.Mock(return_value=expected)

        actual = self.con.post(location)

        self.assertEqual(expected, actual)
        self.con._communicate.assert_called_once_with(
            vmemclient.core.request.PostRequest,
            location, None, None, None)

    def test_put(self):
        expected = GENERIC_SUCCESS
        location = '/some/location'
        self.con._communicate = mock.Mock(return_value=expected)

        actual = self.con.put(location)

        self.assertEqual(expected, actual)
        self.con._communicate.assert_called_once_with(
            vmemclient.core.request.PutRequest,
            location, None, None, None)

    def test_delete(self):
        expected = GENERIC_SUCCESS
        location = '/some/location'
        self.con._communicate = mock.Mock(return_value=expected)

        actual = self.con.delete(location)

        self.assertEqual(expected, actual)
        self.con._communicate.assert_called_once_with(
            vmemclient.core.request.DeleteRequest,
            location, None, None, None)

    def test_communicate(self):
        expected = GENERIC_SUCCESS
        cls_type = mock.Mock()
        location = '/some/location'
        raw_data = None
        get_params = None
        headers = None
        retry = True

        config = {'read.return_value': GENERIC_SUCCESS_AS_JSON_STRING}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)

        self.con._check_response_for_errors = mock.Mock()

        actual = self.con._communicate(cls_type, location, raw_data,
                                       get_params, headers, retry)

        self.assertTrue(expected, actual)

    def test_communicate_retry_with_check_response_for_errors_auth_error(self):
        expected = GENERIC_SUCCESS
        cls_type = mock.Mock()
        location = '/some/location'
        raw_data = None
        get_params = None
        headers = None
        retry = True

        self.con.keepalive = True
        self.con.login = mock.Mock(return_value=True)

        config = {'read.return_value': GENERIC_SUCCESS_AS_JSON_STRING}
        resp = mock.Mock()
        resp.configure_mock(**config)
        self.con._handle.open = mock.Mock(return_value=resp)

        self.con._check_response_for_errors = mock.Mock(
            side_effect=(AuthenticationError, None))

        actual = self.con._communicate(cls_type, location, raw_data,
                                       get_params, headers, retry)

        self.assertEqual(expected, actual)
        self.assertEqual(2, self.con._handle.open.call_count)
        self.assertEqual(2, self.con._check_response_for_errors.call_count)

    def test_communicate_retry_with_httperror_error(self):
        expected = GENERIC_SUCCESS
        cls_type = mock.Mock()
        location = '/some/location'
        raw_data = None
        get_params = None
        headers = None
        retry = True

        self.con.keepalive = True
        self.con.login = mock.Mock(return_value=True)

        config = {'read.return_value': GENERIC_SUCCESS_AS_JSON_STRING}
        ok = mock.Mock()
        ok.configure_mock(**config)
        error = urllib2.HTTPError('http://foo.bar', 403, 'error', {}, None)

        self.con._handle.open = mock.Mock(side_effect=(error, ok))

        self.con._check_response_for_errors = mock.Mock()

        actual = self.con._communicate(cls_type, location, raw_data,
                                       get_params, headers, retry)

        self.assertEqual(expected, actual)
        self.assertEqual(2, self.con._handle.open.call_count)

    def test_check_response_for_errors_using_dict_with_no_error(self):
        value = GENERIC_SUCCESS
        response = self.con._check_response_for_errors(value)

        self.assertTrue(response is None)

    def test_check_response_for_errors_using_string_with_no_error(self):
        value = 'some string with no errors'
        response = self.con._check_response_for_errors(value)

        self.assertTrue(response is None)

    def test_check_response_for_errors_raises_unknown_path_error(self):
        value = INVALID_PATH_RESPONSE
        self.assertRaises(
            UnknownPathError,
            self.con._check_response_for_errors, value)

    def test_check_response_for_errors_raises_missing_parameter_error(self):
        value = 'some error string\n{"success":false,"msg":"missing param"}'

        self.assertRaises(
            MissingParameterError,
            self.con._check_response_for_errors, value)

    def test_check_response_for_errors_raises_authentication_error(self):
        value = {'code': 'unauthorized'}

        self.assertRaises(
            AuthenticationError,
            self.con._check_response_for_errors, value)

    def test_check_response_for_errors_raises_rest_action_failed_error(self):
        value = {'code': 'failed', 'msg': 'foo'}

        self.assertRaises(
            RestActionFailed,
            self.con._check_response_for_errors, value)

    def test_get_version_info(self):
        version_number = '7.5.5'
        build_number = 1234
        expected = {
            'version': '{0}.{1}'.format(version_number, build_number),
            'build': build_number,
            'concerto_version': version_number,
            'api_version': '',
        }

        return_value = {
            'success': True,
            'msg': 'Success',
            'data': expected,
        }
        self.con.get = mock.Mock(return_value=return_value)

        actual = self.con._get_version_info()

        self.assertEqual(expected, actual)

    def test_create_login_url(self):
        ans = self.con._create_login_url()

        result = urllib2.urlparse.urlsplit(self.con._create_login_url())

        self.assertTrue(result is not None)

    def test_create_login_data(self):
        login_data = self.con._create_login_data()

        self.assertTrue(login_data)
        self.assertTrue(isinstance(login_data, basestring))
        self.assertTrue('username' in login_data)
        self.assertTrue('password' in login_data)

    def test_process_login_response(self):
        expected = {'id': '123-456-abc-def'}
        self.con._url = None

        return_value = self.con._process_login_response(expected)

        self.assertTrue(return_value is None)
        self.assertEqual(expected, self.con.login_info)
        self.assertTrue(self.con._url is not None)

    def test_close(self):
        self.con.post = mock.Mock(return_value=None)

        return_value = self.con.close()

        self.assertTrue(return_value is None)
        self.assertTrue(self.con.closed)
        self.assertTrue(self.con.login_info is None)

    def test_close_no_rerun_on_single_call_authentication_error(self):
        self.con.post = mock.Mock(return_value=None)
        self.con.keepalive = True

        return_value = self.con.close()

        self.assertTrue(return_value is None)
        self.assertTrue(self.con.post.call_count != 2)
        self.assertTrue(self.con.closed)
        self.assertTrue(self.con.login_info is None)

    def test_close_can_be_called_multiple_times(self):
        self.con.post = mock.Mock(return_value=None)

        return_value1 = self.con.close()
        return_value2 = self.con.close()

        self.assertTrue(return_value1 is None)
        self.assertTrue(return_value2 is None)
        self.assertTrue(self.con.closed)
        self.assertTrue(self.con.login_info is None)

    def test_update_properties(self):
        expected = PROPERTIES_DATA['data']
        self.con.get = mock.Mock(return_value=PROPERTIES_DATA)

        return_value = self.con.update_properties()

        self.assertTrue(return_value is None)
        self.assertEqual(expected, self.con._properties)
