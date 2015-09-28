import asyncio
from aiohttp import web
from aiohttp_ac_hipchat.oauth2 import Oauth2Client
from aiohttp_ac_hipchat.util import http_request
import logging
import base64
import json

INSTALLABLE_PATH = '/installable'

_log = logging.getLogger(__name__)

def _invalid_install(message):
    _log.error("Installation failed: %s" % message)
    return web.HTTPBadRequest(reason=message)

def add_installable_handlers(addon, allow_room=True, allow_global=True, send_events=True,
        validate_group=None, scopes=None):

    app = addon.app

    @asyncio.coroutine
    def on_install(request):

        install_scopes = scopes({}) if callable(scopes) else scopes
        base64_data = request.match_info.get("base64_data")
        if base64_data:
            data = base64.urlsafe_b64decode(base64_data.encode("utf-8"))
            json_data = json.loads(data.decode("utf-8"))
            install_scopes = json_data.get("scopes", install_scopes)

        data = yield from request.json()
        if not data.get('roomId', None) and not allow_global:
            return _invalid_install("This add-on can only be installed in individual rooms.  Please visit the " +
                                    "'Add-ons' link in a room's administration area and install from there.")

        if data.get('roomId', None) and not allow_room:
            return _invalid_install("This add-on cannot be installed in an individual room.  Please visit the " +
                                    "'Add-ons' tab in the 'Group Admin' area and install from there.")

        _log.info("Retrieving capabilities doc at %s" % data['capabilitiesUrl'])
        with (yield from http_request('GET', data['capabilitiesUrl'], timeout=10)) as resp:
            capdoc = yield from resp.read(decode=True)

        if capdoc['links'].get('self', None) != data['capabilitiesUrl']:
            return _invalid_install("The capabilities URL %s doesn't match the resource's self link %s" %
                                    (data['capabilitiesUrl'], capdoc['links'].get('self', None)))

        _log.info("Receiving installation of id {oauthId}".format(oauthId=data['oauthId']))

        client = Oauth2Client(data['oauthId'], data['oauthSecret'], 
                              room_id=data.get('roomId', None), 
                              capdoc=capdoc,
                              scopes=install_scopes,
                              cache=app['redis_pool'])

        try:
            session = yield from client.get_token(token_only=False)
        except Exception as e:
            _log.warn("Error validating installation by receiving token: %s" % e)
            return _invalid_install("Unable to retrieve token using the new OAuth information")

        if validate_group:
            err = validate_group(int(session['group_id']))
            if err:
                return _invalid_install(err)

        store = app['addon_client_store']
        yield from store.delete(None, client.id)

        client.group_id = session['group_id']
        client.group_name = session['group_name']
        yield from store.set(None, client.to_map(), client.id)

        if send_events:
            yield from addon.fire_event('install', {"client": client})

        return web.HTTPCreated()

    @asyncio.coroutine
    def on_uninstall(request):
        store = app['addon_client_store']

        oauth_id = request.match_info['oauth_id']
        client = yield from addon.load_client(oauth_id)
        yield from store.delete(None, client.id)
        if send_events:
            yield from addon.fire_event('uninstall', {"client": client})

        return web.HTTPNoContent()

    app.router.add_route('POST', '%s' % INSTALLABLE_PATH, on_install)
    app.router.add_route('POST', '%s/{base64_data}' % INSTALLABLE_PATH, on_install)
    
    app.router.add_route('DELETE', '%s/{oauth_id}' % INSTALLABLE_PATH, on_uninstall)
    app.router.add_route('DELETE', '%s/{base64_data}/{oauth_id}' % INSTALLABLE_PATH, on_uninstall)
