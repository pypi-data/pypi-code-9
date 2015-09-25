try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
    import urllib.request as urlrequest
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode
    import urllib2 as urlrequest
import json

API_URL_DEFAULT = 'https://www.hipchat.com/'
FORMAT_DEFAULT = 'json'

class HipChat(object):
    def __init__(self, token=None, url=API_URL_DEFAULT, format=FORMAT_DEFAULT):
        self.url = url
        self.token = token
        self.format = format
        self.opener = urlrequest.build_opener(urlrequest.HTTPSHandler())

    class RequestWithMethod(urlrequest.Request):
        def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, http_method=None):
            urlrequest.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
            if http_method:
                self.method = http_method

        def get_method(self):
            if self.method:
                return self.method
            return urlrequest.Request.get_method(self)

    def method(self, url, method='POST', headers={}, data=None, timeout=None):
        method_url = urljoin(self.url, url)
        req = self.RequestWithMethod(method_url, http_method=method, headers=headers, data=data)
        response = self.opener.open(req, None, timeout).read()

    def message_room(self, room_id='', message='', message_format='text', color='', notify=False, token=''):
        url = 'v2/room/%d/notification' % room_id
        headers = {
              "content-type": "application/json",
              "authorization": "Bearer %s" % token
        }

        data = json.dumps({
          'message': message,
          'color': color,
          'message_format': message_format,
          'notify': notify,
          'from': 'me'
        })

        return self.method(url, headers=headers, data=data)
