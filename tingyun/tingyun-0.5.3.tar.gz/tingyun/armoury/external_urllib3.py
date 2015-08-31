
"""

"""

from tingyun.armoury.ammunition.external_tracker import wrap_external_trace


def detect(module):

    def url_request(request, method, url, *args, **kwargs):
        return url

    wrap_external_trace(module, 'RequestMethods.request', 'urllib3', url_request)
