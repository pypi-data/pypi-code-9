import json
import urllib
import urllib2
from django.conf import settings
from floraconcierge.errors import ApiError


class Chat():
    URL = 'http://floraconcierge.com/:chat/'
    SECRET = getattr(settings, 'FLORACONCIERGE_CHAT_SECRET', None)

    chat_id = None

    def __init__(self, chat=0, name='Unknown name', mail='Unknown email'):
        if chat:
            self.chat_id = chat
            self.response('check_id')
        else:
            self.chat_id = self.response('register', {'name': name, 'email': mail})

    def send(self, message):
        return self.response('send', {'message': message.encode('utf-8')})

    def get(self, last_id):
        return self.response('get', {'last_id': last_id})

    def last_id(self):
        return self.response('last_id')

    def response(self, action, post=None):
        params = {
            '_secret': self.SECRET,
            '_action': action,
        }
        if action != 'register':
            params['_chat_id'] = self.chat_id
        url = self.URL + '?' + urllib.urlencode(params)
        req = urllib2.Request(url, urllib.urlencode(post) if post else None)
        result = urllib2.urlopen(req).read()
        result = json.loads(result)
        if result.get('error'):
            raise ApiError(result.get('error'))
        return result['result']
