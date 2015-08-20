from tingyun.api.platform import six
from tingyun.api.tracert.external_trace import wrap_external_trace


def detect(module):

    def url_opener_open(opener, fullurl, *args, **kwargs):
        if isinstance(fullurl, six.string_types):
            return fullurl
        else:
            return fullurl.get_full_url()

    wrap_external_trace(module, 'OpenerDirector.open', 'urllib2', url_opener_open)