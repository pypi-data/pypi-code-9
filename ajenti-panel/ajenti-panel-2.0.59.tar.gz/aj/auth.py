import json
import logging
import pexpect
import pwd
import subprocess
import syslog
from jadi import component, service, interface

import aj
from aj.api.http import BaseHttpHandler
from aj.security.verifier import ClientCertificateVerificator
from aj.util import public


@public
class SudoError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


@public
@service
class AuthenticationMiddleware(BaseHttpHandler):
    def __init__(self, context):
        self.context = context
        self.auth = AuthenticationService.get(self.context)
        if not hasattr(context, 'identity'):
            context.identity = None

    def handle(self, http_context):
        if http_context.env['SSL_CLIENT_VALID']:
            if not self.context.identity:
                username = http_context.env['SSL_CLIENT_USER']
                logging.info(
                    'SSL client certificate %s verified as %s',
                    http_context.env['SSL_CLIENT_DIGEST'],
                    username
                )
                try:
                    pwd.getpwnam(username)
                    found = True
                except KeyError:
                    found = False
                if found:
                    self.auth.login(username)

        http_context.add_header('X-Auth-Identity', str(self.context.identity or ''))


class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


@interface
class AuthenticationProvider(object):
    id = None
    name = None
    allows_sudo_elevation = False

    def __init__(self, context):
        self.context = context

    def authenticate(self, username, password):
        raise NotImplementedError

    def get_isolation_uid(self, username):
        raise NotImplementedError


@component(AuthenticationProvider)
class OSAuthenticationProvider(AuthenticationProvider):
    id = 'os'
    name = 'OS users'
    allows_sudo_elevation = True

    def authenticate(self, username, password):
        child = None
        try:
            child = pexpect.spawn('/bin/sh', ['-c', '/bin/su -c "/bin/echo SUCCESS" - %s' % username], timeout=5)
            child.expect('.*:')
            child.sendline(password)
            result = child.expect(['su: .*', 'SUCCESS'])
        except Exception as err:
            if child and child.isalive():
                child.close()
            logging.error('Error checking password: %s', err)
            return False
        if result == 0:
            return False
        else:
            return True

    def get_isolation_uid(self, username):
        return pwd.getpwnam(username).pw_uid


@public
@service
class AuthenticationService(object):
    def __init__(self, context):
        self.context = context

    def get_provider(self):
        provider_id = aj.config.data['auth'].get('provider', 'os')
        for provider in AuthenticationProvider.all(self.context):
            if provider.id == provider_id:
                return provider
        raise AuthenticationError('Authentication provider %s is unavailable' % provider_id)

    def check_password(self, username, password):
        return self.get_provider().authenticate(username, password)

    def check_sudo_password(self, username, password):
        if not aj.config.data['auth'].get('allow_sudo', False):
            return False
        sudo = subprocess.Popen(
            ['sudo', '-S', '-u', 'eugene', '--', 'sh', '-c', 'sudo -k; sudo -S echo'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        o, e = sudo.communicate(password + '\n')
        if sudo.returncode != 0:
            raise SudoError((o + e).splitlines()[-1].strip())
        return True

    def check_persona_assertion(self, assertion, audience):
        import requests
        
        params = {
            'assertion': assertion,
            'audience': audience,
        }

        resp = requests.post('https://verifier.login.persona.org/verify', data=params, verify=True)

        if resp.ok:
            verification_data = json.loads(resp.content)
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                return email
            else:
                raise AuthenticationError('Persona auth failed')
        else:
            raise AuthenticationError('Request failed')

    def client_certificate_callback(self, connection, x509, errno, depth, result):
        if depth == 0 and (errno == 9 or errno == 10):
            return False  # expired / not yet valid
        if not aj.config.data['ssl']['client_auth']['force']:
            return True
        user = ClientCertificateVerificator.get(aj.context).verify(x509)
        return bool(user)

    def get_identity(self):
        return self.context.identity

    def login(self, username, demote=True):
        logging.info('Authenticating session as %s', username)
        syslog.syslog(syslog.LOG_NOTICE | syslog.LOG_AUTH, '%s has logged in from %s' % (
            username,
            self.context.session.client_info['address'],
        ))
        if demote:
            uid = self.get_provider().get_isolation_uid(username)
            logging.debug('Authentication provider "%s" maps "%s" -> %i' % (
                self.get_provider().name,
                username,
                uid,
            ))
            self.context.worker.demote(uid)
        self.context.identity = username

    def prepare_session_redirect(self, http_context, username):
        http_context.add_header('X-Session-Redirect', username)
