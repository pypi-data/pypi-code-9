import json


def http_rpc_endpoint(url, method_prefix=None, **kwargs):
    return Endpoint(HttpPostTransport(url, **kwargs), method_prefix)


class BadRequestConstructionError(Exception):
    pass


class BadJsonRpcParametersError(Exception):
    pass


class RemoteError(Exception):
    def __init__(self, code, message, data):
        super().__init__(code, message, data)
        self.code = code
        self.data = data
        self.message = message


def _set_id(item, id):
    item.update({'id': id})


class _RequestSender():
    def __init__(self, transport, message_id_counter):
        self.transport = transport
        self.get__next_message_id = message_id_counter

    def _send(self, payload, async):
        if async is False:
            for item in payload:
                _set_id(item, self.get__next_message_id())

        synchronous_response = \
            self.transport.send(json.dumps(payload if len(payload) > 1 else payload[0]))

        if synchronous_response:
            response = json.loads(synchronous_response)
            if not isinstance(response, list):
                response = [response]

            response.sort(key=lambda x: x['id'])

            result = []

            for item in response:
                try:
                    result.append(item['result'])
                except KeyError:
                    error = item['error']
                    result.append(RemoteError(
                                code=error['code'],
                                message=error['message'],
                                data=error.get('data', None)))

            if len(result) == 1:
                return self._unwrap_single_result(result)
            else:
                return result

    def _unwrap_single_result(self, result):
            result = result[0]
            if isinstance(result, Exception):
                raise result
            else:
                return result


class _JsonRpcMethod():
    def __init__(self, name, message_sender, method_prefix):
        self.name = name
        self.message_sender = message_sender
        self.method_prefix = method_prefix

    def __call__(self, *args, async=False, **kwargs):
        if args and kwargs:
            raise BadJsonRpcParametersError()

        params = args if args else kwargs
        data = {
            'jsonrpc': '2.0',
            'method': '{prefix}{name}'.format(prefix=self.method_prefix, name=self.name)
        }

        if params:
            data['params'] = params

        return self.message_sender._send([data], async)


class _BatchRequestBuilder():
    def __init__(self, message_sender, method_prefix):
        self.message_sender = message_sender
        self.method_prefix = method_prefix
        self.payloads = []

    def _send(self, payload, *args, **kwargs):
        self.payloads.extend(payload)
        return self

    def send(self, async=False):
        return self.message_sender._send(self.payloads, async)

    def __getattr__(self, attr):
        return _JsonRpcMethod(attr, self, self.method_prefix)


class Endpoint():
    def __init__(self, message_sender, method_name_prefix=None):
        self.message_sender = \
            _RequestSender(message_sender, self._next_message_id)
        self.method_prefix = method_name_prefix
        self.message_id = 0

    def batch(self):
        return \
            _BatchRequestBuilder(self.message_sender, self.method_prefix or '')

    def __getattr__(self, attr):
        return _JsonRpcMethod(
                attr,
                self.message_sender,
                self.method_prefix or '')

    def _next_message_id(self):
        self.message_id += 1
        return self.message_id


class HttpPostTransport():
    def __init__(self, endpoint_url, headers=None):
        import requests
        self.endpoint_url = endpoint_url
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def send(self, payload):
        response = self.session.post(self.endpoint_url, data=payload)
        response.raise_for_status()
        if response.text:
            print("respnse.text={}".format(response.text))
            return response.text
