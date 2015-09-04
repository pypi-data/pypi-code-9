import asyncio
from aiohttp import web
from aiohttp_ac_hipchat.oauth2 import Oauth2Client
from aiohttp_ac_hipchat.util import http_request
import logging

_log = logging.getLogger(__name__)

def _invalid_install(message):
    _log.error("Installation failed: %s" % message)
    return web.HTTPBadRequest(reason=message)

def add_installable_handlers(app, base_path="", allow_room=True, allow_global=True, send_events=True,
        coll_name='clients', validate_group=None, scopes=None):

    @asyncio.coroutine
    def on_install(request):
        addon = app['addon']

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
                              scopes=scopes)

        try:
            session = yield from client.get_token(app['redis_pool'], token_only=False)
        except Exception as e:
            _log.warn("Error validating installation by receiving token: %s" % e)
            return _invalid_install("Unable to retrieve token using the new OAuth information")

        if validate_group:
            err = validate_group(int(session['group_id']))
            if err:
                return _invalid_install(err)

        clients = app['mongodb'].default_database[coll_name]
        client.group_id = session['group_id']
        client.group_name = session['group_name']
        yield from clients.remove(client.id_query)
        yield from clients.insert(client.to_map())
        if send_events:
            yield from addon.fire_event('install', {"client": client})

        return web.HTTPCreated()

    app.router.add_route('POST', '/installable', on_install)

    @asyncio.coroutine
    def on_uninstall(request):
        addon = app['addon']

        oauth_id = request.match_info['oauth_id']
        client = yield from addon.load_client(oauth_id)
        clients = app['mongodb'].default_database[coll_name]
        yield from clients.remove(client.id_query)
        if send_events:
            yield from addon.fire_event('uninstall', {"client": client})

        return web.HTTPNoContent()

    app.router.add_route('DELETE', '/installable/{oauth_id}', on_uninstall)
