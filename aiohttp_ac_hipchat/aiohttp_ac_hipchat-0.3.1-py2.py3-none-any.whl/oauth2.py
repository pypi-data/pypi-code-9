from aiohttp_ac_hipchat.cache import NoOpCache
from aiohttp_ac_hipchat.room_client import RoomClient
import jwt
import logging
import asyncio
from aiohttp_ac_hipchat.util import http_request

_log = logging.getLogger(__name__)

ACCESS_TOKEN_CACHE = "hipchat-tokens:{oauth_id}"

no_op_cache = NoOpCache()

class Oauth2Client:

    def __init__(self, id, secret=None, homepage=None, capabilities_url=None, room_id=None, token_url=None,
                 group_id=None, group_name=None, capdoc=None, scopes=None, cache=None):
        self.id = id
        self.room_id = room_id
        self.secret = secret
        self.group_id = group_id
        self.group_name = None if not group_name else group_name
        self.homepage = homepage or None if not capdoc else capdoc['links']['homepage']
        self.token_url = token_url or None if not capdoc else capdoc['capabilities']['oauth2Provider']['tokenUrl']
        self.capabilities_url = capabilities_url or None if not capdoc else capdoc['links']['self']
        self.scopes = set(scopes if scopes else [])
        self.cache = cache if not None else no_op_cache

        self._room_client = None

    def to_map(self):
        return {
            "id": self.id,
            "secret": self.secret,
            "room_id": self.room_id,
            "group_id": self.group_id,
            "group_name": self.group_name,
            "homepage": self.homepage,
            "token_url": self.token_url,
            "capabilities_url": self.capabilities_url,
            "scopes": ",".join(self.scopes)
        }

    @staticmethod
    def from_map(data, cache):
        filtered = {key: val for key, val in data.items() if not key.startswith('_')}
        filtered["scopes"] = set(filtered["scopes"].split(",") if filtered.get("scopes") else [])
        return Oauth2Client(cache=cache, **filtered)

    @property
    def id_query(self):
        return {"id": self.id}

    @property
    def api_base_url(self):
        return self.capabilities_url[0:self.capabilities_url.rfind('/')]

    @property
    def room_base_url(self):
        return "{base_url}/room/{room_id}".format(base_url=self.api_base_url, room_id=self.room_id)

    @property
    def room_client(self):
        if not self._room_client:
            self._room_client = RoomClient(self)

        return self._room_client

    def has_scope(self, scope):
        return scope in self.scopes

    @asyncio.coroutine
    def get_token(self, token_only=True, scopes=None):

        if scopes is None:
            scopes = self.scopes

        cache_key = ACCESS_TOKEN_CACHE.format(oauth_id=self.id)
        cache_key += ":" + ",".join(scopes)

        @asyncio.coroutine
        def gen_token():
            with (yield from http_request('POST', self.token_url, data={
                "grant_type": "client_credentials", "scope": " ".join(scopes)},
                    auth=(self.id, self.secret), timeout=10)) as resp:
                if resp.status == 200:
                    _log.debug("Token request response: %s" % (yield from resp.read()))
                    return (yield from resp.read(decode=True))
                elif resp.status == 401:
                    _log.error("Client %s is invalid but we weren't notified.  Uninstalling" % self.id)
                    raise OauthClientInvalidError(self)
                else:
                    raise Exception("Invalid token: %s" % (yield from resp.read()))

        if token_only:
            token = yield from self.cache.get(cache_key)
            if not token:
                data = yield from gen_token()
                token = data['access_token']
                yield from self.cache.setex(key=cache_key, value=token, seconds=data['expires_in'] - 20)
            return token
        else:
            return (yield from gen_token())

    def sign_jwt(self, user_id, data=None):
        if data is None:
            data = {}
        data.update({
            'iss': self.id,
            'prn': user_id
        })
        return jwt.encode(data, self.secret)


class OauthClientInvalidError(Exception):
    def __init__(self, client, *args, **kwargs):
        super(OauthClientInvalidError, self).__init__(*args, **kwargs)
        self.client = client
