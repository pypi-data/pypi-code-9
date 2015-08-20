from tingyun.api.tracert.external_trace import wrap_external_trace


def detect(module):

    def url_request(request, method, url, *args, **kwargs):
        return url

    wrap_external_trace(module, 'RequestMethods.request_encode_url', 'urllib3', url_request)
    wrap_external_trace(module, 'RequestMethods.request_encode_body', 'urllib3', url_request)
