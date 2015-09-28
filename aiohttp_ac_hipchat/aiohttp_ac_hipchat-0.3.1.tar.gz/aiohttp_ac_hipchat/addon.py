import asyncio
import logging
from aiohttp import web
from aiohttp_ac_hipchat.oauth2 import Oauth2Client
from aiohttp_ac_hipchat.util import not_none, is_request_from_hipchat_server
from functools import wraps
import jwt
import json
import datetime
import base64
import copy
from calendar import timegm
from aiohttp_ac_hipchat.installable import add_installable_handlers, INSTALLABLE_PATH

JWT_LEEWAY_IN_SECONDS = 60 * 5

_log = logging.getLogger(__name__)

def always(context):
    return True

def is_hipchat_server(context):
    return context.get("hipchat_server", False)

class Addon(object):
    def __init__(self, app, allow_room=True, allow_global=False, scopes=None):
        self.app = app
        self.addon_client_store = app["addon_client_store"]
        self.cache = app["cache"]
        self.config = app["config"]
        self.events = {}
        self.scopes = scopes

        name = not_none(self.config, "ADDON_NAME")
        self.key = not_none(self.config, "ADDON_KEY")
        self.base_descriptor = {
            "key": self.key,
            "name": name,
            "description": self.config.get('ADDON_DESCRIPTION', ""),
            "links": {
                "self": self.relative_to_base("/addon/descriptor")
            },
            "capabilities": {
                "installable": {
                    "allowRoom": allow_room,
                    "allowGlobal": allow_global
                },
                "hipchatApiConsumer": {
                    "fromName": self.config.get("ADDON_FROM_NAME", name)
                }
            },
            "vendor": {
                "url": self.config.get('ADDON_VENDOR_URL', ""),
                "name": self.config.get('ADDON_VENDOR_NAME', "")
            }
        }
        self.descriptor_element_providers = []

        add_installable_handlers(self, allow_room=allow_room, allow_global=allow_global, scopes=scopes)

        self.app.router.add_route('GET', '/', self.get_descriptor)

    @asyncio.coroutine
    def get_descriptor(self, request):

        context = yield from self.get_context(request)
        descriptor = yield from self.generate_descriptor(context)

        return web.Response(text=json.dumps(descriptor))

    @asyncio.coroutine
    def get_context(self, request):
        return {
            "hipchat_server": (yield from is_request_from_hipchat_server(request))
        }

    @asyncio.coroutine
    def generate_descriptor(self, context):
        descriptor = copy.deepcopy(self.base_descriptor)

        capabilities = descriptor["capabilities"]
        scopes = yield from self.get_scopes(context)
        capabilities["hipchatApiConsumer"]["scopes"] = scopes
        capabilities["installable"]["callbackUrl"] = self.generate_callback_url(scopes)

        for descriptor_element_provider in self.descriptor_element_providers:
            descriptor_element_provider(descriptor, context)

        return descriptor

    def generate_callback_url(self, scopes):
        installable_data = {
            "scopes": scopes
        }
        base64_installable_data = base64.urlsafe_b64encode(json.dumps(installable_data).encode("utf-8")).decode("utf-8")
        return self.relative_to_base(INSTALLABLE_PATH + "/" + base64_installable_data)

    @asyncio.coroutine
    def get_scopes(self, context):
        if callable(self.scopes):
            return self.scopes(context)

        return self.scopes

    @asyncio.coroutine
    def load_client(self, client_id):
        client_data = yield from self.addon_client_store.get(None, client_id)
        if client_data:
            return Oauth2Client.from_map(client_data, self.cache)
        else:
            return None

    def fire_event(self, name, obj):
        listeners = self.events.get(name, [])
        for listener in listeners:
            try:
                yield from listener(obj)
            except:
                logging.exception("Unable to fire event {name} to listener {listener}".format(
                    name=name, listener=listener
                ))

    def register_event(self, name, func):
        _log.debug("Registering event: " + name)
        self.events.setdefault(name, []).append(func)

    def unregister_event(self, name, func):
        del self.events.setdefault(name, [])[func]

    def event_listener(self, func):
        self.register_event(func.__name__, func)
        return func

    @asyncio.coroutine
    def validate_jwt(self, request):
        signed_request = request.GET.get('signed_request', None) or \
                         request.headers.get("x-acpt") or \
                         request.headers.get("authorization")

        if not signed_request:
            return None, None, None

        unverified_claims = jwt.decode(signed_request, verify=False)
        oauth_id = unverified_claims['iss']

        # The audience claim identifies the intended recipient, according to the JWT spec,
        # but we still allow the issuer to be used if 'aud' is missing.
        # Session JWTs make use of this (the issuer is the add-on in this case)
        audience = unverified_claims.get('aud')
        if audience is not None:
            oauth_id = audience[0]

        client = yield from self.load_client(oauth_id)
        if not client:
            return None, None, None

        data = jwt.decode(signed_request, client.secret, options={"verify_aud": False}, leeway=JWT_LEEWAY_IN_SECONDS)
        return client, data, signed_request

    def require_jwt(self):

        def create_session_token(client, jwt_data):

            now_utc = datetime.datetime.utcnow()
            exp = now_utc + datetime.timedelta(minutes=15)
            payload = {
                'iss': self.key,
                'sub': jwt_data['sub'],
                'iat': timegm(now_utc.utctimetuple()),
                'exp': timegm(exp.utctimetuple()),
                'aud': [client.id],
                'context': jwt_data['context']
            }
            return jwt.encode(payload, client.secret).decode("utf-8")

        def require_jwt_inner(func):
            @asyncio.coroutine
            @wraps(func)
            def inner(*args, **kwargs):
                _log.debug("Validating jwt")
                request = args[0]
                client, data, signed_request = yield from self.validate_jwt(request)
                if client:
                    request.client = client
                    request.jwt_data = data
                    request.signed_request = signed_request
                    request.token = create_session_token(client, data)
                    return (yield from func(*args, **kwargs))
                else:
                    return web.HTTPUnauthorized(text="Unauthorized request, please check the JWT token")

            return inner

        return require_jwt_inner

    def webhook(self, event, name=None, pattern=None, path=None, auth="jwt", condition=always, **kwargs):
        if path is None:
            path = "/event/" + event

        webhook_capability = {
            "event": event,
            "url": self.relative_to_base(path)
        }

        if name is not None:
            webhook_capability["name"] = name

        if pattern is not None:
            webhook_capability["pattern"] = pattern

        if auth is not None:
            webhook_capability["authentication"] = auth

        return self._add_capability("webhook", webhook_capability, condition=condition, method="POST", path=path,
                                    require_jwt=False)

    def _add_capability(self, capability_name, capability, condition=None, method=None, path=None, require_jwt=True):

        def element_provider(descriptor, context):
            if condition(context):
                descriptor["capabilities"].setdefault(capability_name, []).append(capability)

        self.descriptor_element_providers.append(element_provider)

        def decorator(func):

            @asyncio.coroutine
            @wraps(func)
            def inner(request):
                return (yield from func(request))

            decorated_func = inner
            if require_jwt:
                decorated_func = self.require_jwt()(inner)

            self.app.router.add_route(method, path, decorated_func)

            return decorated_func

        return decorator

    def webpanel(self, key, name, location="hipchat.sidebar.right", path=None, condition=is_hipchat_server, **kwargs):
        if path is None:
            path = "/webpanel/" + key

        webpanel_capability = {
            "key": key,
            "name": {
                "value": name
            },
            "url": self.relative_to_base(path),
            "location": location
        }

        return self._add_capability("webPanel", webpanel_capability, condition=condition, method="GET", path=path)

    def dialog(self, key, name, path=None, options=None, condition=is_hipchat_server):
        if path is None:
            path = "/dialog/" + key

        dialog_capability = {
            "key": key,
            "title": {
                "value": name
            },
            "url": self.relative_to_base(path),
        }

        if options is not None:
            dialog_capability["options"] = options

        return self._add_capability("dialog", dialog_capability, condition=condition, method="GET", path=path)

    def glance(self, key, name, icon, icon_hdpi, path=None, target=None, condition=is_hipchat_server):
        if path is None:
            path = "/glance/" + key

        glance_capability = {
            "key": key,
            "name": {
                "value": name
            },
            "icon": {
                "url": icon,
                "url@2x": icon_hdpi
            },
            "queryUrl": self.relative_to_base(path),
            "target": target
        }

        return self._add_capability("glance", glance_capability, condition=condition, method="GET", path=path)

    def add_action_capability(self, action_capability, condition=is_hipchat_server):
        self._add_capability('action', action_capability, condition=condition)

    def relative_to_base(self, path):
        base = self.config['BASE_URL']
        path = '/' + path if not path.startswith('/') else path
        return base + path
