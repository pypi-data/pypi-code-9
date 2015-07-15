#!/usr/bin/env python3.4
#
# Copyright (C) 2001-2007 Jason R. Mastaler <jason@mastaler.com>
#
# This file is part of TMDA.
#
# TMDA is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  A copy of this license should
# be included in the file COPYING.
#
# TMDA is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with TMDA; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# Based on code from Python's (undocumented) smtpd module
# Copyright (C) 2001,2002 Python Software Foundation.


from optparse import OptionGroup, OptionParser

import os
import signal
import socket
import sys
import asynchat
import asyncore
import base64
import random
import time
import re
import logging

logger = logging.getLogger('tmda.ofmipd')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from . import Util
from . import Version

ipauthmapfile = None  # /etc/ipauthmap or ~/.tmda/ipauthmap
opts = None
_authenticator = None
ssl_context = None

# Classes


class Authenticator(object):
    """Base class for authenticators, which determine the validity of an
    authentication attempt based on the authentication data (often a username
    and password). There are two common ways to derive from this:

    1. If the authenticator has access to the plain-text passwords, it can
       provide the _get_password method (and make _has_passwords return True).
       This allows both plain_check and cram_md5_check.
    2. Otherwise, the authenticator provides its own implementation of
       _plain_check, and cram_md5_check is not usable.

    Don't override plain_check, only _plain_check. plain_check is a simple
    wrapper with logging.

    plain_check requires the local address for use in remote authenticators
    where this can be used to determine the remote auth host. Many
    authenticators can ignore this."""

    # Public interface

    # All derived classes should be able to do this.
    def plain_check(self, username, password, localip):
        self._log_attempt(username)
        success = self._plain_check(username, password, localip)
        self._log_result(username, success)
        return success

    def cram_md5_check(self, username, ticket, response):
        self._log_attempt(username)
        success = self._cram_md5_check(username, ticket, response)
        self._log_result(username, success)
        return success

    def has_cram_md5(self):
        return self._has_passwords()

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    # Things that might be overriden in derived classes

    def _plain_check(self, username, password, localip):
        correct_pass = self._get_password(username)
        if correct_pass is None:
            return False
        return password == correct_pass

    def _cram_md5_check(self, username, ticket, response):
        import hmac
        from hashlib import md5

        pw = self._get_password(username)
        if pw is None:
            return False
        ticket = bytes(ticket, 'utf-8')
        digest = hmac.new(pw, ticket, md5).hexdigest()
        logger.debug("cram-md5: response: %r digest: %r\n" % (response, digest))
        return digest == response

    # Override _has_passwords and _get_password in Authenticators that have
    # access to plain-text passwords in order to support CRAM-MD5.
    def _get_password(self, username):
        return None

    def _has_passwords(self):
        return False

    # Logging methods are private, and probably don't need to be bothered
    # with in derived classes.

    def _log_attempt(self, username):
        logger.info('Authentication attempt for user %r using %r', username,
                    self)

    def _log_result(self, username, success):
        if success:
            result = 'succeeded'
        else:
            result = 'failed'
        logger.info('Authentication %s for user %r using %r', result, username,
                    self)


class ChainAuthenticator(Authenticator):
    """A special-case authenticator that allows multiple authenticators to be
    chained together. Each is checked in turn, and if any one succeeds in
    authenticating the user then the attempt is successful.

    This breaks the rules by overriding plain_check and cram_md5_check. This
    produces the correct behavior by letting the individual authenticators
    do their own logging.
    """

    def __init__(self, auths=None):
        if auths is None:
            auths = []
        Authenticator.__init__(self)

        self._auths = list(auths)

    def plain_check(self, username, password, localip):
        return self.any('plain_check', username, password, localip)

    def cram_md5_check(self, username, ticket, response):
        return self.any('cram_md5_check', username, ticket, response)

    def _has_passwords(self):
        return self.all('_has_passwords')

    def any(self, meth_name, *args, **kwargs):
        for auth in self._auths:
            method = getattr(auth, meth_name)
            if method(*args, **kwargs):
                return True
        else:
            return False

    def all(self, meth_name, *args, **kwargs):
        for auth in self._auths:
            method = getattr(auth, meth_name)
            if not method(*args, **kwargs):
                return False
        else:
            return True

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._auths)


class FileAuthenticator(Authenticator):
    def __init__(self, filename):
        Authenticator.__init__(self)

        mode = Util.getfilemode(filename)
        if mode not in (0o400, 0o600):
            raise IOError('authfile "%s" must be chmod 400 or 600!', filename)

        self._filename = filename

    def _get_password(self, username):
        return self._authdict().get(username.lower())

    def _has_passwords(self):
        return True

    def _authdict(self):
        """Iterate over a tmda-ofmipd authentication file, and return a
        dictionary containing username:password pairs.  Username is
        returned in lowercase."""
        authdict = {}
        fp = open(self._filename, 'r')
        for line in fp:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            (username, password) = line.split(':', 1)
            authdict[username.lower().strip()] = password.strip()
        fp.close()
        return authdict

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._filename)


class PamAuthenticator(Authenticator):
    # XXX There's a significant problem here if the PAM service imposes a
    # delay on failure. This would block all connected clients. Linux-PAM
    # has a way to control this, but it's not in Python PAM.
    # A work-around would be to use a PAM service that does not impose a
    # failure delay (e.g., uses pam_unix with the nodelay option).
    def __init__(self, service='login'):
        Authenticator.__init__(self)
        self._service = service

    def _plain_check(self, username, password, localip):
        # FIXME: PAM is aka PyPAM and is unmaintained (but still shipped in dbian
        #        and ubuntu).  To get all the pypi dependencies correct, this
        #        should be ported to use https://pypi.python.org/pypi/python-pam/1.8.2
        #        or the like
        return False  # fail closed
        import pam as PAM

        auth = PAM.pam()
        conv = lambda auth, msg, appdata: self._conv(msg, password)
        auth.start(self._service, username, conv)
        try:
            auth.authenticate()
            auth.acct_mgmt()
        except PAM.error:
            logger.info('PAM error:', exc_info=True)
            return False

        return True

    def _conv(self, msgs, password):
        import pam as PAM

        result = []
        for (msg, style) in msgs:
            if style == PAM.PAM_PROMPT_ECHO_OFF:
                logger.debug('PAM password prompt (hopefully): %r', msg)
                result.append((password, 0))
            else:
                logger.warning('Unhandled PAM message, style = %d, msg = %s',
                               style, msg)
                result.append(('', 0))
        return result

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._service)


class CheckpwAuthenticator(Authenticator):
    """authprog should return 0 for auth ok, and a positive integer in
    case of a problem."""
    def __init__(self, cmd):
        Authenticator.__init__(self)
        self._cmd = cmd

    def _plain_check(self, username, password, localip):
        cmd = "/bin/sh -c 'exec %s 3<&0'" % self._cmd
        try:
            Util.runcmd_checked(cmd, '%s\0%s\0' % (username, password))
            return True
        except:
            logger.info('authprog %r for user %s failed:', self._cmd, username,
                        exc_info=True)
            return False

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._cmd)


class RemoteAuthenticator(Authenticator):
    def __init__(self, host, port):
        Authenticator.__init__(self)
        self._host = host
        self._port = port
        self._authmap = None

    def remote_address(self, localip):
        address = self._host
        port = None

        if address == '0.0.0.0':
            # This is a feature that seems to be undocumented. It allows
            # remote authentication address:port to be based on the address
            # for the interface that receives the connection.
            if self._authmap is None:
                addrdict = self._addrdict(ipauthmapfile)
            (address, port) = addrdict.get(localip, ('127.0.0.1', None))

        if port is None:
            port = self._port

        return (address, port)

    @staticmethod
    def _addrdict(filename):
        '''Read IP address mappings from a file. Each line defines a mapping
        from an IP address to an IP address with an optional port. Empty lines
        are ignored, and #-prefixed line comments are discarded. Each mapping
        has the form:

          ADDRESS1 <space> ADDRESS2 [ <space> PORT ]

        <space> is any sequence of whitespace characters (except newlines).
        Alternatively, if both addresses are IPv4, an older form is supported:

          IPV4ADDRESS1 : IPV4ADDRESS2 [ : PORT ]

        The first form works for both IPv4 and IPv6, and is preferred.

        Returns a dict mapping ADDRESS1 to (ADDRESS2, PORT) tuples, where PORT
        may be an integer or None.'''

        comment_matcher = re.compile(r'#.*$')
        space_matcher = re.compile(r'\s+')
        ipauthmap = {}
        try:
            fp = open(filename, 'r')
            line_num = 0
            for line in fp:
                line_num += 1

                # Remove trailing comment
                line = comment_matcher.sub('', line)
                line = line.strip()
                if line == '':
                    continue

                pieces = space_matcher.split(line)
                if len(pieces) == 1:
                    # Old-style ip:ip[:port] line
                    pieces = line.split(':')

                if len(pieces) not in (2, 3):
                    logger.error('Format error in ipauthmap file, line %d',
                                 line_num)
                    continue

                (key, val_ip) = pieces[:2]
                # port may be specified or unspecified.
                if len(pieces) > 2:
                    try:
                        val_port = int(pieces[2])
                        if not (0 <= val_port <= 0xFFFF):
                            raise ValueError('Not a valid port number')
                    except ValueError:
                        logger.error('Invalid port in ipauthmap file, line %d',
                                     line_num)
                        continue
                else:
                    val_port = None
                ipauthmap[key] = (val_ip, val_port)
            fp.close()
        except IOError:
            pass

        return ipauthmap


class ImapAuthenticator(RemoteAuthenticator):
    def __init__(self, host, port, secure):
        RemoteAuthenticator.__init__(self, host, port)
        self._secure = secure

    def _plain_check(self, username, password, localip):
        import imaplib

        if self._secure:
            IMAP = imaplib.IMAP4_SSL
        else:
            IMAP = imaplib.IMAP4
        (host, port) = self.remote_address(localip)
        try:
            imap = IMAP(host, port)
            imap.login(username, password)
            imap.logout()
            return True
        except (IMAP.error, socket.error):
            logger.debug('imap(s) authentication failure details:',
                         exc_info=True)
        return False

    def __repr__(self):
        name = self.__class__.__name__
        return '%s(%r, %r, %r)' % (name, self._host, self._port, self._secure)


class Pop3Authenticator(RemoteAuthenticator):
    def __init__(self, host, port, use_apop):
        RemoteAuthenticator.__init__(self, host, port)
        self._use_apop = use_apop

    def _plain_check(self, username, password, localip):
        import poplib

        (host, port) = self.remote_address(localip)
        try:
            pop = poplib.POP3(host, port)
            if self._use_apop:
                pop.apop(username, password)
            else:
                pop.user(username)
                pop.pass_(password)
            pop.quit()
            return True
        except (poplib.error_proto, socket.error):
            logger.debug('pop3 authentication failure details:', exc_info=True)

        return False

    def __repr__(self):
        name = self.__class__.__name__
        return '%s(%r, %r, %r)' % (name, self._host, self._port, self._use_apop)


class LdapAuthenticator(RemoteAuthenticator):
    def __init__(self, host, port, dn):
        try:
            import ldap
        except ImportError:
            msg = 'python-ldap (http://www.python-ldap.org/) required.'
            raise ImportError(msg)
        del ldap
        try:
            dn % ''
        except TypeError:
            raise ValueError("LDAP URL must conain a '%s' placeholder")

        RemoteAuthenticator.__init__(self, host, port)
        self._dn = dn

    def _plain_check(self, username, password, localip):
        import ldap

        (host, port) = self.remote_address(localip)
        try:
            ldap_obj = ldap.initialize('ldap://%s:%s' % (host, port))
            ldap_obj.simple_bind_s(self._dn % username, password)
            ldap_obj.unbind_s()
            return True
        except ldap.LDAPError:
            logger.debug('ldap authentication failure details:', exc_info=True)

        return False

    def __repr__(self):
        name = self.__class__.__name__
        return '%s(%r, %r, %r)' % (name, self._host, self._port, self._dn)


class AuthOptions(object):
    _opt_map = {
        '-A'         : CheckpwAuthenticator,
        '--authprog' : CheckpwAuthenticator,
        '-a'         : FileAuthenticator,
        '--authfile' : FileAuthenticator,
        '-m'         : PamAuthenticator,
        '--pamauth'  : PamAuthenticator,
    }

    def __init__(self):
        self._auths = []

    # add_auth and add_remote_auth are designed as optparse callbacks.
    def add_auth(self, option, opt_str, value, parser):
        auth_class = self._opt_map.get(opt_str)
        if auth_class is None:
            raise StandardError('Unhandled option: %s' % opt_str)
        self._auths.append(auth_class(value))

    def add_remote_auth(self, option, opt_str, value, parser):
        (proto, host, port, path) = self.split_url(value)

        if port is None:
            port = defaultauthports.get(proto)

        if proto == 'imap':
            auth = ImapAuthenticator(host, port, secure=False)
        elif proto == 'imaps':
            auth = ImapAuthenticator(host, port, secure=True)
        elif proto == 'pop3':
            auth = Pop3Authenticator(host, port, use_apop=False)
        elif proto == 'apop':
            auth = Pop3Authenticator(host, port, use_apop=True)
        elif proto == 'ldap':
            auth = LdapAuthenticator(host, port, path)
        else:
            raise ValueError('Unsupported URL scheme: %s' % proto)

        self._auths.append(auth)

    @classmethod
    def split_url(cls, url):
        '''return ('proto', 'host', port, 'path')'''
        result = Util.urlsplit(url, allow_fragments=False)
        # Originally this method included everything following the path as part
        # of the "path" result, and excluded the leading slash. Mimic that
        # behavior.
        if result.query:
            path = '%s?%s' % (result.path, result.query)
        else:
            path = result.path

        if path.startswith('/'):
            path = path[1:]

        return (result.scheme, result.hostname, result.port, path)

    def authenticator(self):
        if len(self._auths) == 0:
            return None
        elif len(self._auths) == 1:
            return self._auths[0]
        else:
            return ChainAuthenticator(self._auths)


class SMTPSession(asynchat.async_chat):
    COMMAND = 0
    DATA = 1
    AUTH = 2

    ac_in_buffer_size = 16384

    def __init__(self, conn, process_msg_func):
        # Base class __init__ calls

        asynchat.async_chat.__init__(self, conn)

        # Save our own __init__ parameters

        self.__conn = conn
        self.__process_msg_func = process_msg_func

        # Initialize object state

        self.set_terminator(b'\r\n')
        self.init_static_state()
        self.init_dynamic_state()

        # Debug tracing

        logger.info('New session %r for %r connected to %r', self, self.__peer,
                    self._local)

    def handle_close(self, error=None):
        if error is None:
            err_info = ('', '')
        else:
            err_info = (' with error ', repr(error))
        logger.debug('Closing session %r%s%s.', self, *err_info)

        asynchat.async_chat.handle_close(self)

        logger.debug('Socket map following session close: %r',
                     asyncore.socket_map)

    def init_static_state(self):
        """Initialize 'static state' - that state which is associated
        solely with the object, or the physical network connection.
        In particular, this state is not flushed by STARTTLS."""

        # If we're running under tcpserver, then it sets up a bunch of
        # environment variables that give socket address information.
        # We always use this, rather than e.g. calling getsockname on
        # conn, because the tcpserver socket might not be passed directly
        # to tmda-ofmipd. For example, stunnel might terminate the socket,
        # decrypt the data and send it here over a pipe...
        # Note: Whilst tcpserver does provide these variables, the
        # xinetd/stunnel combination does not.
        if opts.one_session and 'TCPREMOTEIP' in os.environ:
            self.__peerip = os.environ['TCPREMOTEIP']
            self.__peername = os.environ.get('TCPREMOTEHOST', None)
            if not self.__peername:
                self.__peername = socket.getfqdn(self.__peerip)
            self.__peerport = os.environ['TCPREMOTEPORT']
            self.__peer = (self.__peerip, self.__peerport)

            self._localip = os.environ['TCPLOCALIP']
            self._localname = os.environ.get('TCPLOCALHOST', None)
            if not self._localname:
                self._localname = socket.getfqdn(self._localip)
            self._localport = os.environ['TCPLOCALPORT']
            self._local = (self._localip, self._localport)
        else:
            # xinetd (or stunnel?) does at least provide REMOTE_HOST.
            if opts.one_session and 'REMOTE_HOST' in os.environ:
                self.__peerip = os.environ['REMOTE_HOST']
                self.__peerport = ''
                self.__peer = (self.__peerip, self.__peerport)
            else:
                self.__peer = self.__conn.getpeername()
                self.__peerip = self.__peer[0]
                self.__peerport = self.__peer[1]
            self.__peername = socket.getfqdn(self.__peerip)
            self._local = self.__conn.getsockname()
            self._localip = self._local[0]
            self._localname = socket.getfqdn(self._localip)
            self._localport = self._local[1]

        # Set the TCPLOCALIP environment variable to support
        # VPopMail's reverse IP domain mapping.
        os.environ['TCPLOCALIP'] = self._localip

    def init_dynamic_state(self):
        """Initialize 'dynamic state' - that state which must be flushed
        when a STARTLS command is issued, according to the RFC."""

        # SMTP AUTH
        self.__smtpauth = 0
        self.__auth_resp1 = None
        self.__auth_resp2 = None
        self.__auth_username = None
        self.__auth_sasl = None
        self.__sasl_types = ['login', 'plain']
        # Only some authenticators support cram-md5, because it requires
        # that the authenticator has access to the plain-text password.
        # See FAQ 5.8.
        if _authenticator.has_cram_md5():
            self.__sasl_types.append('cram-md5')
        self.__auth_cram_md5_ticket = '<%s.%s@%s>' % (random.randrange(10000),
                                                      int(time.time()), FQDN)
        self.__line = []
        self.__state = self.COMMAND
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = ''

    def _is_loopback(self, addr):
        '''Return True if addr is a loopback address.'''
        if self.__conn.family == socket.AF_INET6:
            # IPv6. According to RFC 5156, only ::1 (though this can be written
            # in many ways).
            return (socket.inet_pton(socket.AF_INET6, addr) ==
                    socket.inet_pton(socket.AF_INET6, '::1'))
        elif self.__conn.family == socket.AF_INET:
            # IPv4. RFC 5735 says the entire 127.0.0.0/8 block is for the local
            # host.
            return addr.startswith('127.')

        return False

    def start(self):
        self.push('220 %s ESMTP tmda-ofmipd' % FQDN)

    def auth_methods(self):
        return self.__sasl_types

    def service_extensions(self):
        result = []
        allowed_auths = self.auth_methods()
        if allowed_auths:
            allowed_auths_s = ' '.join([s.upper() for s in allowed_auths])
            result.append('AUTH ' + allowed_auths_s)
        return result

    def recv_header_extra(self):
        return ''

    # Make sure the command is valid given the current state. Override
    # in derived classes if restrictions apply. Unimplemented commands
    # need not be checked here.
    def valid_command(self, cmd, arg):
        return True

    # Overrides base class for convenience
    def push(self, msg):
        line = msg
        if type(line) == type(''):
            line = bytes(line, 'utf-8', 'replace')
        elif type(line) != type(b''):
            raise Exception("Bad argument type to push()! Need str or bytes, got %r." % type(line))
        logger.debug('S: %r', line)
        asynchat.async_chat.push(self, line + b'\r\n')

    # Implementation of base class abstract method
    def collect_incoming_data(self, data):
        #self.__line.append(data.decode('ASCII', 'ignore'))
        self.__line.append(data)

    # Implementation of base class abstract method
    def found_terminator(self):
        line = b''.join(self.__line)
        logger.debug('C: %r', line)
        line = line.decode('ascii', 'ignore')
        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            command, arg = (line.split(' ', 1) + [None])[:2]
            command = command.upper()
            if not self.valid_command(command, arg):
                return
            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented' % command)
                return
            method(arg)
            return
        elif self.__state == self.DATA:
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 2821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text.startswith('.'):
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)

            overquota = False
            if opts.throttlescript:
                (overquota, out, err) = Util.runcmd(
                    '%s %s' % (opts.throttlescript, self.__auth_username))

            if overquota:
                status = '450 Outgoing mail quota exceeded'
            else:
                try:
                    self.__process_msg_func(self.__peer,
                                            self.__mailfrom,
                                            self.__rcpttos,
                                            self.__data,
                                            self.__auth_username)
                    status = '250 Ok'
                except:
                    logger.exception("process_message raised an exception")
                    raise

            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator(b'\r\n')
            self.push(status)
        elif self.__state == self.AUTH:
            if line == '*':
                # client canceled the authentication attempt
                self.push('501 AUTH exchange cancelled')
                self.auth_reset_state()
                return
            if self.__auth_resp1 is None:
                self.__auth_resp1 = line
            else:
                self.__auth_resp2 = line
            self.auth_challenge()
        else:
            self.push('451 Internal confusion')
            return

    # factored
    def __getaddr(self, keyword, arg):
        address = None
        keylen = len(keyword)
        if arg[:keylen].upper() == keyword:
            address = arg[keylen:].strip()
            if not address:
                pass
            elif address[0] == '<' and address[-1] == '>' and address != '<>':
                # Addresses can be in the form <person@dom.com> but watch out
                # for null address, e.g. <>
                address = address[1:-1]
        return address

    # Authentication methods

    def verify_login(self, b64username, b64password):
        """The LOGIN SMTP authentication method is an undocumented,
        unstandardized Microsoft invention.  Needed to support MS
        Outlook clients."""
        try:
            username = b64_decode(b64username)
            password = b64_decode(b64password)
        except:
            return 501
        self.__auth_username = username.lower()
        if _authenticator.plain_check(self.__auth_username, password,
                                      self._localip):
            return 1
        else:
            return 0

    def verify_plain(self, response):
        """PLAIN is described in RFC 2595."""
        try:
            response = b64_decode(response)
        except:
            return 501
        try:
            username, username, password = response.split(b'\0')
        except ValueError:
            return 0
        username = username.decode('ascii', 'ignore')
        password = password.decode('ascii', 'ignore')
        self.__auth_username = username.lower()
        if _authenticator.plain_check(self.__auth_username, password,
                                      self._localip):
            return 1
        else:
            return 0

    def verify_cram_md5(self, response, ticket):
        """CRAM-MD5 is described in RFC 2195."""
        try:
            response = b64_decode(response)
        except:
            return 501
        try:
            username, hexdigest = response.split()
        except ValueError:
            return 0
        self.__auth_username = username.lower()
        if _authenticator.cram_md5_check(self.__auth_username, ticket,
                                         hexdigest):
            return 1
        else:
            return 0

    def auth_reset_state(self):
        """As per RFC 2554, the SMTP state is reset if the AUTH fails,
        and once it succeeds."""
        self.__auth_sasl = None
        self.__auth_resp1 = None
        self.__auth_resp2 = None
        self.__state = self.COMMAND

    def auth_notify_required(self):
        """Send a 530 reply.  RFC 2554 says this response may be
        returned by any command other than AUTH, EHLO, HELO, NOOP,
        RSET, or QUIT. It indicates that server policy requires
        authentication in order to perform the requested action."""
        self.push('530 Error: Authentication required')

    def auth_notify_fail(self, failcode=0):
        if failcode == 501:
            # base64 decoding failed
            self.push('501 malformed AUTH input')
        else:
            self.push('535 AUTH failed')
        self.__smtpauth = 0

    def auth_notify_succeed(self):
        self.push('235 AUTH successful')
        os.environ['LOGIN'] = self.__auth_username
        self.__smtpauth = 1

    def auth_verify(self, sasl=None):
        if sasl is None:
            sasl = self.__auth_sasl
        verify = 0
        if sasl == 'plain':
            verify = self.verify_plain(self.__auth_resp1)
        elif sasl == 'cram-md5':
            verify = self.verify_cram_md5(self.__auth_resp1,
                                          self.__auth_cram_md5_ticket)
        elif sasl == 'login':
            verify = self.verify_login(self.__auth_resp1, self.__auth_resp2)
        if verify == 1:
            self.auth_notify_succeed()
        else:
            self.auth_notify_fail(verify)
        self.auth_reset_state()

    def auth_challenge(self):
        if self.__auth_resp1 is None:
            # No initial response, issue first server challenge
            if self.__auth_sasl == 'plain':
                self.push('334 ')
            elif self.__auth_sasl == 'cram-md5':
                self.push(b'334 ' + b64_encode(self.__auth_cram_md5_ticket))
            elif self.__auth_sasl == 'login':
                self.push('334 VXNlcm5hbWU6')
            return
        if self.__auth_resp2 is None:
            # Client sent an initial response
            if self.__auth_sasl in ('plain', 'cram-md5'):
                # Perform authentication
                self.auth_verify()
            elif self.__auth_sasl == 'login':
                # Issue second server challenge
                self.push('334 UGFzc3dvcmQ6')
            return
        # Client sent a second response (only if AUTH=LOGIN),
        # perform authentication
        self.auth_verify()

    # ESMTP/SMTP commands

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: EHLO hostname')
            return

        responses = [FQDN] + self.service_extensions()
        for r in responses[:-1]:
            self.push('250-' + r)
        self.push('250 ' + responses[-1])

        # Put a Received header string in the environment for tmda-inject
        # to add later.
        rh = []
        rh.append('from %s' % (arg))
        pname = self.__peername
        if (arg.lower() != pname.lower()) and (pname.lower() != self.__peerip):
            rh.append('(%s [%s])' % (pname, self.__peerip))
        else:
            rh.append('(%s)' % (self.__peerip))
        extra = self.recv_header_extra()
        if extra:
            rh.append(extra)
        rh.append('by %s (tmda-ofmipd) with ESMTP;' % (FQDN))
        rh.append(Util.make_date())
        os.environ['TMDA_OFMIPD_RECEIVED'] = ' '.join(rh)

    def smtp_NOOP(self, arg):
        if arg:
            self.push('501 Syntax: NOOP')
        else:
            self.push('250 Ok')

    def smtp_QUIT(self, arg):
        # args is ignored
        self.push('221 Bye')
        self.close_when_done()

    def smtp_MAIL(self, arg):
        # Authentication required first
        if not self.__smtpauth:
            self.auth_notify_required()
            return
        logger.info('===> MAIL %s', arg)
        address = self.__getaddr('FROM:', arg)
        if not address:
            self.push('501 Syntax: MAIL FROM:<address>')
            return
        if self.__mailfrom:
            self.push('503 Error: nested MAIL command')
            return
        self.__mailfrom = address
        logger.info('sender: %s', self.__mailfrom)
        self.push('250 Ok')

    def smtp_RCPT(self, arg):
        logger.info('===> RCPT %s', arg)
        if not self.__mailfrom:
            self.push('503 Error: need MAIL command')
            return
        address = self.__getaddr('TO:', arg)
        if not address:
            self.push('501 Syntax: RCPT TO: <address>')
            return
        self.__rcpttos.append(address)
        logger.info('recips: %s', self.__rcpttos)
        self.push('250 Ok')

    def smtp_RSET(self, arg):
        if arg:
            self.push('501 Syntax: RSET')
            return
        # Resets the sender, recipients, and data, but not the greeting
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = ''
        self.__state = self.COMMAND
        self.push('250 Ok')

    def smtp_DATA(self, arg):
        if not self.__rcpttos:
            self.push('503 Error: need RCPT command')
            return
        if arg:
            self.push('501 Syntax: DATA')
            return
        self.__state = self.DATA
        self.set_terminator(b'\r\n.\r\n')
        self.push('354 End data with <CR><LF>.<CR><LF>')

    def smtp_AUTH(self, arg):
        """RFC 2554 - SMTP Service Extension for Authentication"""
        if self.__smtpauth:
            # After an successful AUTH, no more AUTH commands may be
            # issued in the same session.
            self.push('503 Duplicate AUTH')
            return
        if arg:
            args = arg.split()
            if len(args) == 2:
                self.__auth_sasl = args[0]
                self.__auth_resp1 = args[1]
            else:
                self.__auth_sasl = args[0]
        if self.__auth_sasl:
            self.__auth_sasl = self.__auth_sasl.lower()
        if not arg or self.__auth_sasl not in self.auth_methods():
            self.push('504 AUTH type unimplemented')
            return
        self.__state = self.AUTH
        self.auth_challenge()


# SSL Support

# SSL-capable socket wrapper class. The more similar this is to Python 2.6
# SSLSockets, the better.
class SSLSocket(object):
    def __init__(self, sock, ssl_context):
        self._ssl_context = ssl_context
        self._sock = sock
        self._ssl_conn = None

    def do_handshake(self):
        import OpenSSL.SSL as SSL

        if self._ssl_conn is None:
            self._ssl_conn = SSL.Connection(self._ssl_context, self._sock)
            self._ssl_conn.set_accept_state()

    def want_write(self):
        if self._ssl_conn is not None:
            return self._ssl_conn.want_write()
        return False

    # Socket methods

    def __getattr__(self, name):
        if self._ssl_conn is not None:
            return getattr(self._ssl_conn, name)
        else:
            return getattr(self._sock, name)


class CallbackProducer(object):
    """
    A producer for async_chat that produces no data, but calls a provided
    function instead.
    """
    def __init__(self, function):
        self._function = function

    def more(self):
        self._function()
        return b''


class SecureSMTPSession(SMTPSession):
    _start_ssl_values = (
        'immediate',      # An SSL connection
        'optional',       # STARTTLS optional
        'localoptional',  # STARTTLS required except for local connections
        'required',       # STARTTLS required
        'done',           # STARTTLS finished
    )

    def __init__(self, conn, ssl_context, process_msg_func, start_ssl):
        self._ssl_sock = SSLSocket(conn, ssl_context)
        if start_ssl not in self._start_ssl_values:
            raise ValueError('invalid start_ssl argument')
        self._ssl_state = start_ssl

        SMTPSession.__init__(self, self._ssl_sock, process_msg_func)

        if self._ssl_state == 'immediate':
            self.start_ssl()
        elif self._ssl_state == 'localoptional':
            if self._is_loopback(self._localip):
                self._ssl_state = 'optional'
            else:
                self._ssl_state = 'required'

    def start_ssl(self):
        self._ssl_sock.do_handshake()

    # Overrides from SMTPSession

    def auth_methods(self):
        if self._ssl_state == 'required':
            # Must do STARTTLS before AUTH is allowed
            return []

        return SMTPSession.auth_methods(self)

    def service_extensions(self):
        result = SMTPSession.service_extensions(self)
        if self._ssl_state in ('required', 'optional'):
            result.append('STARTTLS')
        return result

    def recv_header_extra(self):
        if self._ssl_state == 'immediate':
            return '(using SMTP over TLS)'
        elif self._ssl_state == 'done':
            return '(using STARTTLS)'
        return ''

    def valid_command(self, cmd, arg):
        if self._ssl_state == 'required':
            valid_cmds = ['NOOP', 'EHLO', 'STARTTLS', 'QUIT']
            if not (cmd in valid_cmds):
                self.push('530 Must issue a STARTTLS command first')
                return False

        return SMTPSession.valid_command(self, cmd, arg)

    # Overrides from asyncore.dispatcher

    def readable(self):
        # Reading could be necessary at any time, for SSL protocol negotiation.
        return True

    def writable(self):
        return self._ssl_sock.want_write() or SMTPSession.writable(self)

    def handle_error(self):
        import OpenSSL.SSL as SSL

        e = sys.exc_info()[1]
        if isinstance(e, (SSL.WantReadError, SSL.WantWriteError)):
            # These non-errors happen frequently, just indicating that the
            # underlying SSL layer needs to do reading or writing on the socket
            # for protocol purposes, blocking general communication in the
            # interim.
            pass
        elif isinstance(e, SSL.Error):
            self.handle_close(e)
        else:
            SMTPSession.handle_error(self)

    # SMTP commands

    def smtp_STARTTLS(self, arg):
        """RFC 3207 - SMTP Service Extension for Secure SMTP over
        Transport Layer Security"""
        if self._ssl_state not in ('required', 'optional'):
            # Not TLS mode, or we have already done STARTTLS
            self.push('503 Duplicate or disallowed STARTTLS')
            return
        if arg:
            self.push('501 Syntax error (no parameters allowed)')
            return
        # XXX There's a chance that the callbacks could happen before the
        # response is sent, which would be bad. It looks like this can't
        # actually happen based on the async_chat implementation. A method
        # that doesn't rely on implementation details would be better.
        self.push('220 Ready to start TLS')
        self.push_with_producer(CallbackProducer(self.start_ssl))
        self.push_with_producer(CallbackProducer(self.init_dynamic_state))
        self._ssl_state = 'done'


class SMTPServer(asyncore.dispatcher):
    """Run an SMTP server daemon - accept new socket connections and
    process SMTP sessions on each connection."""
    def __init__(self, localaddr, session_factory, family=socket.AF_INET):
        self._localaddr = localaddr
        self._session_factory = session_factory
        asyncore.dispatcher.__init__(self)
        self.create_socket(family, socket.SOCK_STREAM)
        # try to re-use a server port if possible
        self.set_reuse_addr()
        self.bind(localaddr)
        self.listen(5)
        logger.info('Listening on %s:%d', *localaddr)

    def readable(self):
        if len(asyncore.socket_map) > opts.connections:
            # too many simultaneous connections
            return 0
        else:
            return 1

    def handle_accept(self):
        conn = self.accept()[0]
        sess = self._session_factory(conn)
        # Make sure the session handles its own errors.
        try:
            sess.start()
        except:
            sess.handle_error()

    def handle_error(self):
        # Default handle_error terminates the server. Let's not do that.
        logger.warning('Error in SMTPServer:', exc_info=True)


# Utility functions

def b64_encode(s):
    """base64 encoding without the trailing newline."""
    return base64.encodestring(bytes(s, 'ascii'))[:-1]


def b64_decode(s):
    """base64 decoding."""
    return base64.decodestring(bytes(s, 'ascii'))


def process_message_fail(peer, mailfrom, rcpttos, data, auth_username):
    """Debug class which prevents the mail from actually being accepted."""
    raise "Test Exception"


def process_message_vdomain(peer, mailfrom, rcpttos, data, auth_username):
    """This proxy is used only for virtual domain support in a qmail +
    (VPopMail or VMailMgr) environment.  It needs to behave differently from
    the standard TMDA proxy in that authenticated users are not system
    (/etc/passwd) users."""
    # Set up partial tmda-inject command line.
    inject_cmd = [sys.executable, '-m', 'TMDA.inject'] + rcpttos
    userinfo = auth_username.split('@', 1) + ['']
    user, domain = userinfo[:2]
    # If running as uid 0, fork in preparation for running the tmda-inject
    # process and change UID and GID to the virtual domain user.  This is
    # for VMailMgr, where each virtual domain is a system (/etc/passwd)
    # user.
    if running_as_root:
        pid = os.fork()
        if pid != 0:
            rpid, status = os.wait()
            # Did tmda-inject succeed?
            if status != 0:
                raise IOError('tmda-inject failed!')
            return
        else:
            # The 'prepend' is the system user in charge of this virtual
            # domain.
            prepend = Util.getvdomainprepend(auth_username,
                                             opts.vdomainspath)
            if not prepend:
                logger.error('Error: "%s" is not a virtual domain', domain)
                sys.exit(-1)
            os.seteuid(0)
            os.setgid(Util.getgid(prepend))
            os.setgroups(Util.getgrouplist(prepend))
            os.setuid(Util.getuid(prepend))
            # For VMailMgr's utilities.
            os.environ['HOME'] = Util.gethomedir(prepend)
    # From here on, we're either in the child (pid == 0) or we're not
    # running as root, so we haven't forked.
    vhomedir = Util.getvuserhomedir(user, domain, opts.vhomescript)
    logger.info('vuser homedir: "%s"', vhomedir)
    # This is so "~" will work in the .tmda/* files.
    os.environ['HOME'] = vhomedir
    # change inject_cmd to pass the message through if
    # --pure-proxy was specified and the .tmda/config file is
    # missing.
    cfgfile = os.path.join(vhomedir, '.tmda', 'config')
    if opts.pure_proxy and not os.path.exists(cfgfile):
        cmd = os.environ.get('TMDA_SENDMAIL_PROGRAM') or '/usr/sbin/sendmail'
        inject_cmd = [cmd, '-f', mailfrom, '-i', '--'] + rcpttos
    try:
        Util.runcmd_checked(inject_cmd, data)
    except Exception:
        logger.exception('Error running injection command')
        if running_as_root:
            sys.exit(-1)
    if running_as_root:
        # Should never get here!
        sys.exit(0)


def process_message_sysuser(peer, mailfrom, rcpttos, data, auth_username):
    """Using this server for outgoing smtpd, the authenticated user
    will have his mail tagged using his TMDA config file."""
    configdir = opts.configdir or '~' + auth_username
    tmda_configdir = os.path.join(os.path.expanduser(configdir), '.tmda')
    tmda_configfile = os.path.join(tmda_configdir, 'config')
    if opts.pure_proxy and not os.path.exists(tmda_configfile):
        cmd = os.environ.get('TMDA_SENDMAIL_PROGRAM') or '/usr/sbin/sendmail'
        inject_cmd = [cmd, '-f', mailfrom, '-i', '--'] + rcpttos
    else:
        inject_cmd = [sys.executable, '-m', 'TMDA.inject']
        inject_cmd += ['-c', tmda_configfile] + rcpttos

    # Set HOME so "~" will always work in the .tmda/* files.
    # gethomedir() is no good in unit tests.
    os.environ['HOME'] = os.environ.get('TMDA_TEST_HOME')
    if not os.environ['HOME']:
        os.environ['HOME'] = Util.gethomedir(auth_username)

    # If running as uid 0, fork the tmda-inject process, and
    # then change UID and GID to the authenticated user.
    if running_as_root:
        pid = os.fork()
        if pid == 0:
            os.seteuid(0)
            os.setgid(Util.getgid(auth_username))
            os.setgroups(Util.getgrouplist(auth_username))
            os.setuid(Util.getuid(auth_username))
            try:
                Util.runcmd_checked(inject_cmd, data)
            except Exception:
                logger.exception('Error running injection command')
                sys.exit(-1)
            sys.exit(0)
        else:
            rpid, status = os.wait()
            # Did tmda-inject succeed?
            if status != 0:
                raise IOError('tmda-inject failed!')
    else:
        # no need to fork
        Util.runcmd_checked(inject_cmd, data)


def create_smtp_session_from_stdin(session_factory):
    conn = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
    sess = session_factory(conn)
    sess.start()


def sig_handler(sig_num, frame):
    sys.exit()


# Main code begins


# Constants
defaultauthports = {'imap': 143,
                    'imaps': 993,
                    'apop': 110,
                    'pop3': 110,
                    'ldap': 389,
                    # 'pop3s': 995,
                    }

NEWLINE = '\n'


# Runtime global variables

program = sys.argv[0]

__version__ = Version.TMDA

FQDN = socket.getfqdn()
if FQDN == 'localhost':
    FQDN = socket.gethostname()

if os.getuid() == 0:
    running_as_root = True
else:
    running_as_root = False


# Option parsing

opt_desc = \
"""An authenticated ofmip proxy for TMDA that allows you to 'tag' your
mail client's outgoing mail through SMTP.  For more information,
including setup and usage instructions, see
http://wiki.tmda.net/TmdaOfmipdHowto"""

parser = OptionParser(description=opt_desc, version=Version.TMDA,
                      formatter=Util.HelpFormatter())

parser.add_option("-V",
                  action="store_true", default=False, dest="full_version",
                  help="show full TMDA version information and exit.")


# general
gengroup = OptionGroup(parser, "General")

gengroup.add_option("-d", "--debug",
                    action="store_true", default=False, dest="debug",
                    help="Turn on debugging prints.")

gengroup.add_option("-L", "--log",
                    action="store_true", default=False, dest="log",
                    help= \
"""Turn on logging prints.
This option logs everything that -d logs, except for the raw SMTP protocol
data. Hence, it is useful if you want to leave logging enabled permanently,
but don't want your logs bloated with AUTH data and/or the content of large
attachments.""")

gengroup.add_option("-b", "--background",
                    action="store_false", dest="foreground",
                    help="Detach and run in the background (default).")

gengroup.add_option("-f", "--foreground",
                    action="store_true", default=False, dest="foreground",
                    help="Don't detach; run in the foreground.")

gengroup.add_option("-u", "--username",
                    dest="username",
                    help= \
"""The username that this program should run under.  The default is to
run as the user who starts the program unless that is root, in which
case an attempt to seteuid user 'tofmipd' will be made.  Use this
option to override these defaults.""")

gengroup.add_option("-c", "--configdir",
                    metavar="DIR", dest="configdir",
                    help= \
"""DIR is the base directory to search for the authenticated user's TMDA
configuration file in.  This might be useful if you wish to maintain
TMDA files outside the user's home directory.
'username/config' will be appended to form the path; e.g, `-c
/var/tmda' will have tmda-ofmipd search for `/var/tmda/bobby/config'.
If this option is not used, `~user/.tmda/config' will be assumed, but
see the --vhome-script option for qmail virtual domain users.""")

# connection
congroup = OptionGroup(parser, "Connection")

congroup.add_option("-p", "--proxyport", action="append",
                    metavar="HOST:PORT", help=
"""The HOST:PORT to listen for incoming connections on.  The default is
FQDN:8025 (i.e, port 8025 on the fully qualified domain name for the
local host).  Use ':PORT' to listen on all available interfaces.""")

congroup.add_option("-6", "--ipv6proxyport", action="append",
                    metavar="HOST:PORT",
                    help="Same as --proxyport, but using IPv6.")

congroup.add_option("-C", "--connections",
                    type="int", default="20", metavar="NUM", dest="connections",
                    help= \
"""Do not handle more than NUM simultaneous connections. If there are NUM
active connections, defer acceptance of new connections until one
finishes. NUM must be a positive integer. Default: 20""")

congroup.add_option("-1", "--one-session",
                    action="store_true", default=False, dest="one_session",
                    help= \
"""Don't bind to a port and accept new connections; Process a single SMTP
session on stdin (used both for input & output).  This is useful when
started from tcpserver or stunnel.""")

congroup.add_option("-P", "--pure-proxy",
                    action="store_true", default=False, dest="pure_proxy",
                    help= \
"""Proxy the message straight through to the mail transport system
unaltered if the user's TMDA config file is missing.  The
/usr/sbin/sendmail program on the system is used to inject the
message.  You can override this by setting $TMDA_SENDMAIL_PROGRAM in
the environment.  This option might be useful when serving a mixed
environment of TMDA and non-TMDA users.""")

congroup.add_option("-t", "--throttle-script",
                    metavar="/PATH/TO/SCRIPT", dest="throttlescript",
                    help= \
"""Full pathname of a script which can meter how much mail any user
sends.  The script is passed a login name whenever a user tries to
send mail.  If the script returns a 0, the message is allowed.  For
any other value, the message is rejected.""")

congroup.add_option("--ssl",
                    action="store_true", default=False, dest="ssl",
                    help= \
"""Enable SSL encryption. This mode immediately initiates the SSL/TLS
protocol as soon as a connection is made. This mode is not support
for the STARTTLS command. This configuration is typically run on
port 465 (smtps).""")

congroup.add_option("--tls",
                    type="choice", default=None, dest="tls",
                    choices=['optional', 'localoptional', 'on'],
                    help= \
"""Enable TLS mode. Valid options are optional, localoptional and on.
With this option enabled, the STARTTLS SMTP command may be used to upgrade
the plain-text connection to SSL/TLS. This protects the safety of plain-text
authentication methods, and message content. This is typically run on port
587 (submission). The different options have the following effect:

  +---------------+------------------+------------+
  |               | AUTH allowed     | AUTH after |
  |               | before STARTTLS? | STARTTLS?  |
  +---------------+------------------+------------+
  | optional      | yes              | yes        |
  +---------------+------------------+------------+
  | localoptional | connections from | yes        |
  |               | localhost only   |            |
  +---------------+------------------+------------+
  | on            | no               | yes        |
  +---------------+------------------+------------+
""")

congroup.add_option("--ssl-cert",
                    metavar="/PATH/TO/FILE", default=None, dest="ssl_cert",
                    help= \
"""Location of the SSL/TLS certificate file. This file may include a chain of
certificates to send, and must be PEM-encoded.""")

congroup.add_option("--ssl-key",
                    metavar="/PATH/TO/FILE", default=None, dest="ssl_key",
                    help= \
"""Location of the SSL/TLS private key file.""")

# Rationale for the default cipher list: Initially, we want to eliminate SSL2
# because it is insecure. 'DEFAULT:!SSLv2' would do this, but also includes weak
# 56- and 40-bit ciphers. That may be fine, but we can be more secure by default
# without sacrificing functionality (because users can restore any ciphers they
# need) if we limit it to HIGH and MEDIUM ciphersuites. However, each of these
# sets includes some ciphersuites without authentication, so we additionally
# exclude them with !aNULL.
congroup.add_option("--ciphers",
                    default="HIGH:MEDIUM:!aNULL:!SSLv2", help=\
"""Set of ciphers to use for secure connections. The format and available names
are given in the OpenSSL manual page ciphers(1). The default is %default. Using
!SSLv2 somewhere in the string is recommended to disable SSL2, which is a
deprecated and insecure protocol.""")

# authentication
authgroup = OptionGroup(parser, "Authentication",
"""Any number of authentication options can be supplied, and they will be
attempted in the order given.""")
auth_options = AuthOptions()

authgroup.add_option("-R", "--remoteauth",
                     metavar="PROTO://HOST[:PORT][/DN]", action="callback",
                     callback=auth_options.add_remote_auth, type="string",
                     help= \
"""Protocol and host to check username and password. PROTO can be one of
the following: 'imap' (IMAP4 server), 'imaps' (IMAP4 server over SSL),
'pop3' (POP3 server), 'apop' (POP3 server with APOP authentication),
'ldap' (LDAP server).  Optional :PORT defaults to the standard port for
the specified protocol (143 for imap, 993 for imaps, 110 for
pop3/apop, and 389 for ldap).  /DN is mandatory for ldap and should
contain a '%s' identifying the username. Examples: '-R
imaps://myimapserver.net', '-R pop3://mypopserver.net:2110', '-R
ldap://example.com/cn=%s,dc=host,dc=com'""")

authgroup.add_option("-A", "--authprog",
                     metavar="PROGRAM", action="callback",
                     callback=auth_options.add_auth, type="string",
                     help= \
"""A checkpassword compatible command used to check username/password.
Examples: '-A "/usr/sbin/checkpassword-pam -s id -- /bin/true"',
'-A "/usr/local/vpopmail/bin/vchkpw /usr/bin/true"'.
The program must be able to receive the username/password pair on
descriptor 3 and in the following format: `username\\0password\\0'
Any program claiming to be checkpassword-compatible should be able to
do this.  If you can tell the program to accept input on another
descriptor, such as stdin, don't.  It won't work, because TMDA follows
the standard (http://cr.yp.to/checkpwd/interface.html) exactly.
Also, checkpassword-type programs expect to find the name of another
program to run on their command line.  For tmda-ofmipd's purpose,
/bin/true is perfectly fine.
Note the position of the quotes in the Examples, which cause the the
whole string following the -A to be passed as a single argument.""")

authgroup.add_option("-a", "--authfile",
                     metavar="FILE", action="callback",
                     callback=auth_options.add_auth, type="string",
                     help= \
"""Path to the file holding authentication information for this proxy.
Default location is /etc/tofmipd if running as root/tofmipd, otherwise
~user/.tmda/tofmipd.  Use this option to override these defaults.""")

authgroup.add_option("-m", "--pamauth",
                     metavar="SERVICE", action="callback",
                     callback=auth_options.add_auth, type="string",
                     help= \
"""Authenticate using system username/password via PAM. Requires
the Python PAM module. The argument is the name of a PAM service, commonly
"login".""")

# virtual domains
virtgroup = OptionGroup(parser, "Virtual Domains")

virtgroup.add_option("-S", "--vhome-script",
                     metavar="/PATH/TO/SCRIPT", dest="vhomescript",
                     help= \
"""Full pathname of a script that prints a virtual email user's home
directory on standard output.  tmda-ofmipd will read that and use it
to build the path to the user's config file instead of '~user/.tmda'.
The script must take two arguments, the user name and the domain, on
its command line.  This option is for use only with the VPopMail and
VMailMgr add-ons to qmail.  See the contrib directory for sample
scripts.""")

virtgroup.add_option("-v", "--vdomains-path",
                     default="/var/qmail/control/virtualdomains",
                     metavar="/PATH/TO/FILE", dest="vdomainspath",
                     help= \
"""Full pathname to qmail's virtualdomains file.  The default is
/var/qmail/control/virtualdomains.  This is also tmda-ofmipd's
default, so you normally won't need to set this parameter.  If you
have installed qmail somewhere other than /var/qmail, you will need to
set this so tmda-ofmipd can find the virtualdomains file.  NOTE: This
is only used when you have a qmail installation with virtual domains
using the VMailMgr add-on.  It implies that you will also set the
'--vhome-script' option above.""")

for g in (gengroup, congroup, authgroup, virtgroup):
    parser.add_option_group(g)

parser.set_defaults(proxyport=[], ipv6proxyport=[])

def handle_opts():
    # The content of this function used to all be at the script scope, so a lot
    # of what it uses are globals.
    global opts
    global _authenticator
    global ipauthmapfile
    global ssl_context

    (opts, args) = parser.parse_args()

    if opts.full_version:
        print(Version.ALL)
        sys.exit()
    if opts.vhomescript and opts.configdir:
        parser.error("options '--vhome-script' and '--configdir' are incompatible!")
    if opts.log:
        logger.setLevel(logging.INFO)
    if opts.debug:
        logger.setLevel(logging.DEBUG)

    _authenticator = auth_options.authenticator()
    if _authenticator is None:
        parser.error('missing authentication option(s)')

    if running_as_root:
        if not opts.username:
            opts.username = 'tofmipd'
        ipauthmapfile = '/etc/ipauthmap'
    else:
        tmda_path = os.path.join(os.path.expanduser('~'), '.tmda')
        ipauthmapfile = os.path.join(tmda_path, 'ipauthmap')

    if opts.ssl or opts.tls:
        if opts.ssl and opts.tls:
            raise ValueError("Can't do SSL and TLS at the same time")

        try:
            import OpenSSL.SSL as SSL
        except ImportError:
            raise ImportError('Python OpenSSL '
                '(http://pyopenssl.sourceforge.net/) required.')

        if not (opts.ssl_cert and opts.ssl_key):
            raise ValueError('--ssl-cert and --ssl-key are required when using --ssl or --tls')

        ssl_context = SSL.Context(SSL.SSLv23_METHOD)
        ssl_context.set_cipher_list(opts.ciphers)
        ssl_context.use_certificate_chain_file(os.path.expanduser(opts.ssl_cert))
        ssl_context.use_privatekey_file(os.path.expanduser(opts.ssl_key))

# provide disclaimer if running as root
if running_as_root:
    logger.warning('WARNING: The security implications and risks of running\n'
                   '%s in "seteuid" mode have not been fully evaluated.\n'
                   'If you are uncomfortable with this, quit now and instead\n'
                   'run it under your non-privileged TMDA user account.',
                   program)

def make_session_factory(process_msg_func):
    if opts.ssl or opts.tls:
        if opts.ssl:
            start_mode = 'immediate'
        elif opts.tls == 'on':
            start_mode = 'required'
        else:
            start_mode = opts.tls

        return lambda conn: SecureSMTPSession(conn, ssl_context,
                                              process_msg_func, start_mode)

    return lambda conn: SMTPSession(conn, process_msg_func)

def main():
    handle_opts()

    if opts.vhomescript:
        session_factory = make_session_factory(process_message_vdomain)
    else:
        session_factory = make_session_factory(process_message_sysuser)

    if opts.one_session:
        create_smtp_session_from_stdin(session_factory)
    else:
        # Add a default address if none were given.
        if opts.proxyport == opts.ipv6proxyport == []:
            opts.proxyport = ["%s:8025" % FQDN]

        logger.info('tmda-ofmipd started at %s', Util.make_date())

        # Try binding to the specified addresses.
        for addr in opts.proxyport:
            host, port = addr.rsplit(':', 1)
            SMTPServer((host, int(port)), session_factory, socket.AF_INET)
        for addr in opts.ipv6proxyport:
            host, port = addr.rsplit(':', 1)
            SMTPServer((host, int(port)), session_factory, socket.AF_INET6)

    # Switch user/group ID, etc.
    if running_as_root:
        # Set group ID
        os.setegid(Util.getgid(opts.username))
        # Set supplemental group ids
        os.setgroups(Util.getgrouplist(opts.username))
        # Set user ID
        os.seteuid(Util.getuid(opts.username))

    # Daemonize the process if required
    if not (opts.foreground or opts.one_session):
        if os.fork() != 0:
            sys.exit()

        if True:
            os.setsid()

            if os.fork() != 0:
                sys.exit()

            os.setpgrp()

            # Theoretically we should close all FDs in
            # range(os.getdtablesize()), but the API doesn't exist!
            os.close(0)
            os.close(1)
            os.close(2)
            os.open('/dev/null', os.O_RDWR | os.O_NOCTTY)
            os.dup(0)
            os.dup(0)
            sys.stdin = os.fdopen(0, 'r')
            sys.stdout = os.fdopen(1, 'w')
            sys.stderr = os.fdopen(2, 'w')

            signal.signal(signal.SIGTSTP, signal.SIG_IGN);
            signal.signal(signal.SIGTTOU, signal.SIG_IGN);
            signal.signal(signal.SIGTTIN, signal.SIG_IGN);

            signal.signal(signal.SIGHUP, sig_handler);
            signal.signal(signal.SIGTERM, sig_handler);

    # Start the event loop
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


# This is the end my friend.
if __name__ == '__main__':
    main()
