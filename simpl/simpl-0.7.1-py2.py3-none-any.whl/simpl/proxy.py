"""Proxy code for simplifying authentication logic on clients.

To use ProxyRouter:


"""

import json
import logging
import re

import bottle
import requests
from six.moves.urllib import parse

from simpl import __about__
from simpl import rest

LOG = logging.getLogger(__name__)


class ProxyRouter():

    """Proxy HTTP Requests.

    Ajax clients  may not be able to talk to auth or other endpoints
    because of limitations such as CORS. This class operates as a proxy
    to allow clients to perform operations like authentication through this
    server.

    This class is intended to be used to handle only a few specific
    requests that are intgral to the operating of our javascript, client
    apps. It is not intended as a general use HTTP proxy.
    """

    def __init__(self, app, allowed_endpoints=None):
        """Wire up a proxy router.

        :keyword list allowed_endpoints: list of URLs to accept calls to.
        """
        if allowed_endpoints:
            self.allowed_endpoints = [re.compile(p) for p in allowed_endpoints]
        else:
            self.allowed_endpoints = []

        self.via = "1.0 Simpl (Simpl/%s)" % __about__.__version__
        self.timeout = 10
        app.route('/proxy/<path:path>', ['POST', 'GET', 'PUT'], self.proxy)

    def dispatch(self, target, request, path=None):
        """Proxy the call to the remote target."""
        parsed_url = parse.urlparse(target)
        root = parsed_url.scheme + "://" + parsed_url.hostname
        for endpoint in self.allowed_endpoints:
            if endpoint.match(root):
                break
        else:
            bottle.abort(403, "Proxy endpoint not permitted: %s" % target)

        if bottle.request.body and getattr(request.body, 'len', -1) > 0:
            auth = rest.read_body(request)
        else:
            auth = None
        headers = {
            'Via': self.via
        }
        token = request.get_header('X-Auth-Token')
        if token:
            headers['X-Auth-Token'] = token
        headers['Content-Type'] = request.content_type or 'application/json'
        headers['Accept'] = request.get_header('Accept', 'application/json')
        headers['User-Agent'] = request.get_header("User-Agent")
        headers['X-Forwarded-For'] = request.remote_addr

        # TODO: implement some caching to not overload auth
        LOG.debug('Proxy call to %s', target)
        post_body = json.dumps(auth) if auth else None
        proxy_path = path or parsed_url.path
        if not proxy_path.startswith('/'):
            proxy_path = '/%s' % proxy_path

        # Prepare proxy call


        try:
            resp = requests.request(request.method, root + proxy_path,
                                    body=post_body, headers=headers)
            http.request(request.method, proxy_path, body=post_body,
                         headers=headers)
            resp = http.getresponse()
            body = resp.read()
        except (KeyboardInterrupt, SystemExit):
            raise  # don't intercept shutdown attempts
        except Exception as exc:
            LOG.error('HTTP connection exception: %s', exc)
            raise bottle.HTTPError(401, output='Unable to communicate with '
                                   'remote server')

        if resp.status != 200:
            try:
                body = json.loads(body)
                if len(body) == 1 and isinstance(body.values()[0], dict):
                    body = body.values()[0]
                for key, value in body.items():
                    if any(k in key for k in ('message', 'msg')):
                        msg = "%s: %s" % (resp.reason, value)
                        break
                else:
                    msg = resp.reason
            except Exception:
                pass
            LOG.debug('Invalid authentication: %s', msg)
            raise bottle.HTTPError(401, output=msg)

        try:
            content = json.loads(body)
        except ValueError:
            msg = "Proxy target did not return a json-encoded body"
            LOG.debug(msg)
            raise bottle.HTTPError(401, output=msg)

        try:  # to detect if we just authenticated an admin
            if self.auth_endpoint == source:
                if any(r for r in
                       content['access']['user'].get('roles')
                       if r['name'] == self.admin_role):
                    LOG.debug("Admin authenticated: %s",
                              content['access']['user'].get('id'))
                    bottle.response.add_header('X-AuthZ-Admin', 'True')
        except StandardError as exc:
            LOG.debug("Ignored error while checking roles: %s", exc)
        return write_body(content, request, bottle.response)


    def proxy(self, path=None):
        """Proxy Requests for a generic endpoint (ex. github)."""
        # Check for source
        source = bottle.request.get_header('X-Proxy')
        if not source:
            bottle.abort(400, "X-Auth-Source or X-Proxy header not supplied. "
                         "The header is required and must point to a valid "
                         "and permitted proxy endpoint.")

        url = parse(source)
        root = url.scheme + "://" + url.hostname
        allowed_domain = False
        for endpoint in self.allowed_endpoints:
            if endpoint.startswith(root):
                allowed_domain = True
                break

        if not allowed_domain:
            bottle.abort(401, "Proxy endpoint not permitted: %s" % source)

        if bottle.request.body and getattr(bottle.request.body, 'len', -1) > 0:
            auth = read_body(bottle.request)
        else:
            auth = None
        host = url.hostname
        headers = {}
        token = bottle.request.get_header('X-Auth-Token')
        if token:
            headers['X-Auth-Token'] = token
        headers['Content-Type'] = bottle.request.get_header('Content-Type',
                                                            'application/json')
        headers['Accept'] = bottle.request.get_header('Accept',
                                                      'application/json')
        headers['X-Forwarded-For'] = bottle.request.remote_addr
        headers['Via'] = "1.0 Waldo (Waldo/0.0.1)"
        headers['User-Agent'] = bottle.request.get_header("User-Agent")

        # TODO: implement some caching to not overload auth
        LOG.debug('Proxy call to %s', source)
        post_body = json.dumps(auth) if auth else None
        proxy_path = path or url.path
        if not proxy_path.startswith('/'):
            proxy_path = '/%s' % proxy_path

        # Prepare proxy call
        if url.scheme == 'https':
            http_class = httplib.HTTPSConnection
            port = url.port or 443
        else:
            http_class = httplib.HTTPConnection
            port = url.port or 80
        http = http_class(host, port, timeout=10)

        try:
            http.request(bottle.request.method, proxy_path, body=post_body,
                         headers=headers)
            resp = http.getresponse()
            body = resp.read()
        except Exception as exc:
            LOG.error('HTTP connection exception: %s', exc)
            raise bottle.HTTPError(401, output='Unable to communicate with '
                                   'keystone server')
        finally:
            http.close()

        if resp.status != 200:
            try:
                body = json.loads(body)
                if len(body) == 1 and isinstance(body.values()[0], dict):
                    body = body.values()[0]
                for key, value in body.items():
                    if any(k in key for k in ('message', 'msg')):
                        msg = "%s: %s" % (resp.reason, value)
                        break
                else:
                    msg = resp.reason
            except Exception:
                pass
            LOG.debug('Invalid authentication: %s', msg)
            raise bottle.HTTPError(401, output=msg)

        try:
            content = json.loads(body)
        except ValueError:
            msg = "Proxy target did not return a json-encoded body"
            LOG.debug(msg)
            raise bottle.HTTPError(401, output=msg)

        try:  # to detect if we just authenticated an admin
            if self.auth_endpoint == source:
                if any(r for r in
                       content['access']['user'].get('roles')
                       if r['name'] == self.admin_role):
                    LOG.debug("Admin authenticated: %s",
                              content['access']['user'].get('id'))
                    bottle.response.add_header('X-AuthZ-Admin', 'True')
        except StandardError as exc:
            LOG.debug("Ignored error while checking roles: %s", exc)
        return write_body(content, bottle.request, bottle.response)

    def authproxy(self, path=None):
        """Proxy calls to a Keystone-like auth endpoint."""
        # Check for source
        source = (bottle.request.get_header('X-Auth-Source') or
                  self.default_auth_endpoint)
        if not source:
            bottle.abort(401, "X-Auth-Source header not supplied. The header "
                         "is required and must point to a valid and permitted "
                         "proxy endpoint.")
        data = self.dispatch(source)


