from datetime import datetime
from dateutil.tz import tzutc
import logging
import json

from requests.auth import HTTPBasicAuth
from requests import sessions

_session = sessions.Session()


def post(key, secret, url = 'https://api.salesmachine.io/v1/batch', **kwargs):
    """Post the `kwargs` to the API"""
    log = logging.getLogger('salesmachine')
    body = kwargs['batch']
    #body["sentAt"] = datetime.utcnow().replace(tzinfo=tzutc()).isoformat()
    auth = HTTPBasicAuth(key, secret)
    data = json.dumps(body, cls=DatetimeSerializer)
    headers = {'content-type': 'application/json'}
    log.debug('making request: %s', data)
    res = _session.post(url, data=data, auth=auth, headers=headers, timeout=15)

    if res.status_code >= 200 and res.status_code < 300:
        log.debug('data uploaded successfully')
        return res

    try:
        payload = res.json()
        log.debug('received response: %s', payload)
        raise APIError(res.status_code, payload['code'], payload['message'])
    except ValueError:
        raise APIError(res.status_code, 'unknown', res.text)


class APIError(Exception):

    def __init__(self, status, code, message):
        self.message = message
        self.status = status
        self.code = code

    def __str__(self):
        msg = "[Salesmachine] {0}: {1} ({2})"
        return msg.format(self.code, self.message, self.status)


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
