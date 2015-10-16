import asyncio
import json
import logging
from aiohttp_ac_hipchat.util import http_request

_log = logging.getLogger(__name__)

REQUEST_TIMEOUT_IN_SECONDS = 10

class RoomClient(object):

    def __init__(self, client):
        self.client = client

    @asyncio.coroutine
    def get_participants(self, room_id_or_name):
        token = yield from self.client.get_token()
        with (yield from http_request('GET',
                                      "{base_url}/room/{room_id_or_name}/participant?expand=items".format(
                                          base_url=self.client.api_base_url,
                                          room_id_or_name=room_id_or_name),
                                      headers={'content-type': 'application/json',
                                               'authorization': 'Bearer %s' % token},
                                      timeout=REQUEST_TIMEOUT_IN_SECONDS)) as resp:
            if resp.status == 200:
                body = yield from resp.read(decode=True)
                return body['items']
            else:
                _log.error("Cannot get participants for room {room_id_or_name}".format(room_id_or_name=room_id_or_name))
                return None

    @asyncio.coroutine
    def create_room(self, name, topic=None, owner_id_or_name=None, guest_access=False, privacy="public"):

        token = yield from self.client.get_token(scopes=['manage_rooms'])

        data = {'name': name,
                'topic': topic,
                'owner_user_id': owner_id_or_name,
                'guest_access': guest_access,
                'privacy': privacy}

        with (yield from http_request('POST',
                                      "{base_url}/room".format(base_url=self.client.api_base_url),
                                      headers={'content-type': 'application/json',
                                               'authorization': 'Bearer %s' % token},
                                      data=json.dumps(data),
                                      timeout=REQUEST_TIMEOUT_IN_SECONDS)) as resp:
            if resp.status != 201:
                body = yield from resp.read()
                _log.error("Cannot create room: %s - %s" % (resp.status, body))
                return False

            body = yield from resp.json()
            return body['id']

    @asyncio.coroutine
    def send_notification(self, from_mention=None, text=None, html=None, room_id_or_name=None,
            color="yellow", notify=False):
        if room_id_or_name is None:
            room_id_or_name = self.client.room_id

        token = yield from self.client.get_token()

        if html:
            data = {"message": html,
                    "message_format": "html"}
        elif text:
            msg = text
            if from_mention:
                msg = "@%s %s" % (from_mention, text)
            data = {"message": msg,
                    "message_format": "text"}
        else:
            raise Exception("'html' or 'text' must be specified")

        valid_colors = ('yellow', 'green', 'red', 'purple', 'gray', 'random')
        if not color.lower() in valid_colors:
            raise Exception("'color' must be one of %s or %s" % (', '.join(valid_colors[0:-1]),
                                                                 valid_colors[-1]))

        data.update({"color": color,
                     "notify": notify})

        with (yield from http_request('POST',
                                      "{base_url}/room/{room_id_or_name}/notification".format(
                                          base_url=self.client.api_base_url,
                                          room_id_or_name=room_id_or_name),
                                      headers={'content-type': 'application/json',
                                               'authorization': 'Bearer %s' % token},
                                      data=json.dumps(data),
                                      timeout=REQUEST_TIMEOUT_IN_SECONDS)) as resp:
            if resp.status != 204:
                body = yield from resp.read()
                _log.error("Cannot send notification: %s - %s" % (resp.status, body))

    @asyncio.coroutine
    def create_webhook(self, url, event='room_message', pattern=None, room_id_or_name=None, name=''):
        if room_id_or_name is None:
            room_id_or_name = self.client.room_id

        data = {
            "url": url,
            "event": event,
            "name": name
        }
        if pattern is not None:
            data['pattern'] = pattern

        token = yield from self.client.get_token(scopes=['admin_room'])
        with (yield from http_request('POST',
                                      "{base_url}/room/{room_id}/webhook".format(
                                          base_url=self.client.api_base_url,
                                          room_id=room_id_or_name),
                                      headers={'content-type': 'application/json',
                                               'authorization': 'Bearer %s' % token},
                                      data=json.dumps(data),
                                      timeout=REQUEST_TIMEOUT_IN_SECONDS)) as resp:
            if resp.status != 201:
                body = yield from resp.read()
                _log.error("Cannot register webhook: %s - %s" % (resp.status, body))
                return False

            return resp.headers.get("LOCATION")

    @asyncio.coroutine
    def delete_webhook(self, url):
        token = yield from self.client.get_token(scopes=['admin_room'])
        with (yield from http_request('DELETE',
                                      url,
                                      headers={'authorization': 'Bearer %s' % token},
                                      timeout=REQUEST_TIMEOUT_IN_SECONDS)) as resp:
            if resp.status != 204:
                body = yield from resp.read()
                _log.error("Cannot unregister webhook: %s - %s" % (resp.status, body))
                return False

        return True
