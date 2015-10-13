import json

import emotient.error


class APIWrapper(object):
    """
    This is a wrapper around the http client that attaches the Emotient-specific headers and content types.
    """
    def __init__(self, api_key, http_client, api_base, api_version):
        self.api_base = api_base
        self.api_key = api_key
        self.http_client = http_client
        self.api_version = api_version

    @property
    def base_url(self):
        return u'{}/v{}'.format(self.api_base, self.api_version)

    def get_headers(self, headers):
        if headers is None:
            headers = {}

        base_headers = {
            'Authorization': self.api_key
        }

        headers.update(base_headers)
        return headers

    def request(self, method, url, headers=None, data=None, params=None, files=None, timeout=10):
        api_url = u'{}/{}'.format(self.base_url, url)
        headers = self.get_headers(headers)

        if data is not None:
            dumped_data = json.dumps(data)
        else:
            dumped_data = None

        content, status_code, headers = self.http_client.request(method, api_url, headers, data=dumped_data,
                                                                 params=params, files=files, timeout=timeout)

        if hasattr(content, 'decode'):
            content = content.decode('utf-8')

        json_content = None
        if 'application/json' in headers.get('content-type') and status_code != 204:
            json_content = json.loads(content)

        if 400 <= status_code < 600:
            exc = emotient.error.get_error(status_code)
            if json_content is not None:
                error_msg = emotient.error.format_error_message(json_content)
            else:
                error_msg = 'Unknown error'
            raise exc(message=error_msg, status_code=status_code, http_content=content)

        if json_content is not None:
            return json_content
        else:
            return content

    def request_json(self, *args, **kwargs):
        content = self.request(*args, **kwargs)

        if not isinstance(content, dict):
            raise emotient.error.EmotientAPIError('Unexpected error: received non-JSON response')

        return content

    def request_to_file(self, fp, method, url, headers=None, params=None, timeout=10):
        api_url = u'{}/{}'.format(self.base_url, url)
        headers = self.get_headers(headers)

        resp_iterator = self.http_client.streaming_request(method, api_url, headers, params=params, timeout=timeout)

        for block in resp_iterator(1024):
            if not block:
                break

            if hasattr(block, 'decode'):
                block = block.decode('utf-8')

            fp.write(block)
        return fp

    def request_page(self, list_url, page, per_page, timeout=10):
        params = {
            'page': page,
            'per_page': per_page
        }
        return self.request_json('GET', list_url, params=params, timeout=timeout)

    def download_aggregated_file(self, fp, url, interval='summary', report='standard', gender='both', timeout=10):
        params = {
            'interval': interval,
            'report': report,
            'gender': gender
        }
        return self.request_to_file(fp, 'GET', url, params=params, timeout=timeout)
