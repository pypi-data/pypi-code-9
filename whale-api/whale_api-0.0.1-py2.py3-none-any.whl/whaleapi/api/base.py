import json
import logging
import time

import requests
import six

from whaleapi.api import backoff_period, max_timeouts
from whaleapi.api.exceptions import (ApiError, ApiNotInitialized, ClientError, HttpBackoff,
                                     HttpTimeout)

log = logging.getLogger(__name__)


class HTTPClient(object):
    backoff_period = backoff_period
    max_timeouts = max_timeouts
    backoff_timestamp = None
    timeout_counter = 0

    @classmethod
    def request(cls, method, path, body=None, response_formatter=None,
                error_formatter=None, **params):

        try:
            if not cls.should_submit():
                raise HttpBackoff("Too many timeouts. Won't try again for {1} seconds."
                                  .format(*cls.backoff_status()))

            from whaleapi.api import api_token, api_host, mute, proxies, max_retries, \
                timeout, cacert

            if api_token is None:
                raise ApiNotInitialized("API token is not set."
                                        " Please run 'initialize' method first.")

            url = "%s/api/%s/" % (api_host, path.lstrip("/"))

            headers = {}
            if isinstance(body, dict):
                body = json.dumps(body)
                headers['Content-Type'] = 'application/json'
                headers['Authorization'] = 'Token %s' % api_token

            start_time = time.time()
            try:
                s = requests.Session()
                http_adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
                s.mount('https://', http_adapter)

                result = s.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    data=body,
                    timeout=timeout,
                    proxies=proxies,
                    verify=cacert)

                result.raise_for_status()
            except requests.ConnectionError as e:
                raise ClientError("Could not request %s %s%s: %s" % (method, api_host, url, e))
            except requests.exceptions.Timeout as e:
                cls.timeout_counter += 1
                raise HttpTimeout('%s %s timed out after %d seconds.' % (method, url, timeout))
            except requests.exceptions.HTTPError as e:
                if e.response.status_code in (403, 404):
                    pass
                else:
                    raise
            except TypeError as e:
                raise TypeError(
                    "Your installed version of 'requests' library seems not compatible with"
                    "Whale's usage. We recommend upgrading it ('pip install -U requests').")

            duration = round((time.time() - start_time) * 1000., 4)
            log.info("%s %s %s (%sms)" % (result.status_code, method, url, duration))
            cls.timeout_counter = 0

            content = result.content

            if content:
                try:
                    if six.PY3:
                        response_obj = json.loads(content.decode('utf-8'))
                    else:
                        response_obj = json.loads(content)
                except ValueError:
                    raise ValueError('Invalid JSON response: {0}'.format(content))

                if response_obj and 'errors' in response_obj:
                    raise ApiError(response_obj)
            else:
                response_obj = None
            if response_formatter is None:
                return response_obj
            else:
                return response_formatter(response_obj)

        except ClientError as e:
            if mute:
                log.error(str(e))
                if error_formatter is None:
                    return {'errors': e.args[0]}
                else:
                    return error_formatter({'errors': e.args[0]})
            else:
                raise
        except ApiError as e:
            if mute:
                for error in e.args[0]['errors']:
                    log.error(str(error))
                if error_formatter is None:
                    return e.args[0]
                else:
                    return error_formatter(e.args[0])
            else:
                raise

    @classmethod
    def should_submit(cls):
        now = time.time()
        should_submit = False

        if not cls.backoff_timestamp and cls.timeout_counter >= cls.max_timeouts:
            log.info("Max number of Whale timeouts exceeded, backing off for {0} seconds"
                     .format(cls.backoff_period))
            cls.backoff_timestamp = now
            should_submit = False

        elif cls.backoff_timestamp:
            backed_off_time, backoff_time_left = cls.backoff_status()
            if backoff_time_left < 0:
                log.info("Exiting backoff state after {0} seconds, will try to submit metrics again"
                         .format(backed_off_time))
                cls.backoff_timestamp = None
                cls.timeout_counter = 0
                should_submit = True
            else:
                log.info("In backoff state, won't submit metrics for another {0} seconds"
                         .format(backoff_time_left))
                should_submit = False
        else:
            should_submit = True

        return should_submit

    @classmethod
    def backoff_status(cls):
        now = time.time()
        backed_off_time = now - cls.backoff_timestamp
        backoff_time_left = cls.backoff_period - backed_off_time
        return round(backed_off_time, 2), round(backoff_time_left, 2)


class CreateableAPIResource(object):
    @classmethod
    def create(cls, method='POST', id=None, params=None, **body):
        if params is None:
            params = {}
        if method == 'GET':
            return HTTPClient.request('GET', cls.class_url, **body)
        if id is None:
            return HTTPClient.request('POST', cls.class_url, body, **params)
        else:
            return HTTPClient.request('POST', cls.class_url + "/" + str(id), body, **params)


class SendableAPIResource(object):
    @classmethod
    def send(cls, id=None, **body):
        if id is None:
            return HTTPClient.request('POST', cls.class_url, body)
        else:
            return HTTPClient.request('POST', cls.class_url + "/" + str(id), body,)


class UpdatableAPIResource(object):
    @classmethod
    def update(cls, id, params=None, **body):
        if params is None:
            params = {}
        return HTTPClient.request('PUT', cls.class_url + "/" + str(id), body, **params)


class DeletableAPIResource(object):
    @classmethod
    def delete(cls, id, **params):
        return HTTPClient.request('DELETE', cls.class_url + "/" + str(id), **params)


class GetableAPIResource(object):
    @classmethod
    def get(cls, id, **params):
        return HTTPClient.request('GET', cls.class_url + "/" + str(id), **params)


class ListableAPIResource(object):
    @classmethod
    def get_all(cls, **params):
        return HTTPClient.request('GET', cls.class_url, **params)


class SearchableAPIResource(object):
    @classmethod
    def search(cls, **params):
        return HTTPClient.request('GET', cls.class_url, **params)
