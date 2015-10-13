import requests
import requests.exceptions

from emotient import error


def get_http_client():
    return RequestsClient()


class HTTPClient(object):

    def request(self, method, url, headers, data=None, params=None, files=None, timeout=10):
        raise NotImplementedError()

    def streaming_request(self, method, url, headers, data=None, params=None, files=None, timeout=10):
        raise NotImplementedError()


class RequestsClient(HTTPClient):

    def _request(self, method, url, headers, data=None, params=None, files=None, timeout=10, stream=False):
        try:
            resp = requests.request(method, url, headers=headers, data=data, params=params, files=files,
                                    timeout=timeout, stream=stream)
        except requests.exceptions.Timeout:
            raise
        except Exception:
            msg = 'Unexpected error while communicating with Emotient.'
            raise error.EmotientAPIError(msg)

        return resp

    def request(self, method, url, headers, data=None, params=None, files=None, timeout=10):
        resp = self._request(method, url, headers, data=data, params=params, files=files, timeout=timeout)
        return resp.content, resp.status_code, resp.headers

    def streaming_request(self, method, url, headers, data=None, params=None, files=None, timeout=10):
        resp = self._request(method, url, headers, data=data, params=params, files=files, timeout=timeout,
                             stream=True)
        return resp.iter_content
