# -*- coding: UTF-8 -*-
##############################################################################
#
#    OdooRPC
#    Copyright (C) 2014 Sébastien Alix.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""This module contains the ``ODOO`` class which is the entry point to manage
an `Odoo` server.
"""
from odoorpc import rpc, error, tools
from odoorpc.env import Environment
from odoorpc import session
from odoorpc.db import DB
from odoorpc.report import Report


class ODOO(object):
    """Return a new instance of the :class:`ODOO` class.
    `JSON-RPC` protocol is used to make requests, and the respective values
    for the `protocol` parameter are ``jsonrpc`` (default) and ``jsonrpc+ssl``.

    .. doctest::
        :options: +SKIP

        >>> import odoorpc
        >>> odoo = odoorpc.ODOO('localhost', protocol='jsonrpc', port=8069)

    `OdooRPC` will try by default to detect the server version in order to
    adapt its requests if necessary. However, it is possible to force the
    version to use with the `version` parameter:

    .. doctest::
        :options: +SKIP

        >>> odoo = odoorpc.ODOO('localhost', version='8.0')

    *Python 2:*

    :raise: :class:`odoorpc.error.InternalError`
    :raise: `ValueError` (wrong protocol, port value, timeout value)
    :raise: `urllib2.URLError` (connection error)

    *Python 3:*

    :raise: :class:`odoorpc.error.InternalError`
    :raise: `ValueError` (wrong protocol, port value, timeout value)
    :raise: `urllib.error.URLError` (connection error)
    """

    def __init__(self, host='localhost', protocol='jsonrpc',
                 port=8069, timeout=120, version=None):
        if protocol not in ['jsonrpc', 'jsonrpc+ssl']:
            txt = ("The protocol '{0}' is not supported by the ODOO class. "
                   "Please choose a protocol among these ones: {1}")
            txt = txt.format(protocol, ['jsonrpc', 'jsonrpc+ssl'])
            raise ValueError(txt)
        try:
            port = int(port)
        except ValueError:
            raise ValueError("The port must be an integer")
        try:
            timeout = int(timeout)
        except ValueError:
            raise ValueError("The timeout must be an integer")
        self._host = host
        self._port = port
        self._protocol = protocol
        self._env = None
        self._login = None
        self._password = None
        self._db = DB(self)
        self._report = Report(self)
        # Instanciate the server connector
        try:
            self._connector = rpc.PROTOCOLS[protocol](
                self._host, self._port, timeout, version)
        except rpc.error.ConnectorError as exc:
            raise error.InternalError(exc.message)
        # Dictionary of configuration options
        self._config = tools.Config(
            self,
            {'auto_commit': True,
             'auto_context': True,
             'timeout': timeout})

    @property
    def config(self):
        """Dictionary of available configuration options.

        .. doctest::
            :options: +SKIP

            >>> odoo.config
            {'auto_commit': True, 'auto_context': True, 'timeout': 120}

        .. doctest::
            :hide:

            >>> 'auto_commit' in odoo.config
            True
            >>> 'auto_context' in odoo.config
            True
            >>> 'timeout' in odoo.config
            True

        - ``auto_commit``: if set to `True` (default), each time a value is set
          on a record field a RPC request is sent to the server to update the
          record (see :func:`odoorpc.env.Environment.commit`).

        - ``auto_context``: if set to `True` (default), the user context will
          be sent automatically to every call of a
          :class:`model <odoorpc.models.Model>` method (default: `True`):

            >>> odoo.env.context['lang'] = 'fr_FR'
            >>> Product = odoo.env['product.product']
            >>> Product.name_get([2])   # Context sent by default ('lang': 'fr_FR' here)
            [[2, 'Surveillance sur site']]
            >>> odoo.config['auto_context'] = False
            >>> Product.name_get([2])   # No context sent, 'en_US' used
            [[2, 'On Site Monitoring']]

        - ``timeout``: set the maximum timeout in seconds for a RPC request
          (default: `120`):

            >>> odoo.config['timeout'] = 300

        """
        return self._config

    @property
    def version(self):
        """The version of the server.

        >>> odoo.version
        '8.0'
        """
        return self._connector.version

    @property
    def db(self):
        """The database management service.
        See the :class:`odoorpc.db.DB` class.
        """
        return self._db

    @property
    def report(self):
        """The report management service.
        See the :class:`odoorpc.report.Report` class.
        """
        return self._report

    host = property(lambda self: self._host,
                    doc="Hostname of IP address of the the server.")
    port = property(lambda self: self._port,
                    doc="The port used.")
    protocol = property(lambda self: self._protocol,
                        doc="The protocol used.")

    @property
    def env(self):
        """The environment which wraps data to manage records such as the
        user context and the registry to access data model proxies.

        >>> Partner = odoo.env['res.partner']
        >>> Partner
        Model('res.partner')

        See the :class:`odoorpc.env.Environment` class.
        """
        self._check_logged_user()
        return self._env


    def json(self, url, params):
        """Low level method to execute JSON queries.
        It basically performs a request and raises an
        :class:`odoorpc.error.RPCError` exception if the response contains
        an error.

        You have to know the names of each parameter required by the function
        called, and set them in the `params` dictionary.

        Here an authentication request:

        .. doctest::
            :options: +SKIP

            >>> data = odoo.json(
            ...     '/web/session/authenticate',
            ...     {'db': 'db_name', 'login': 'admin', 'password': 'admin'})
            >>> from pprint import pprint
            >>> pprint(data)
            {'id': 645674382,
             'jsonrpc': '2.0',
             'result': {'db': 'db_name',
                        'session_id': 'fa740abcb91784b8f4750c5c5b14da3fcc782d11',
                        'uid': 1,
                        'user_context': {'lang': 'en_US',
                                         'tz': 'Europe/Brussels',
                                         'uid': 1},
                        'username': 'admin'}}

        .. doctest::
            :hide:

            >>> data = odoo.json(
            ...     '/web/session/authenticate',
            ...     {'db': DB, 'login': USER, 'password': PWD})
            >>> data['result']['db'] == DB
            True
            >>> data['result']['uid'] == 1
            True
            >>> data['result']['username'] == USER
            True

        And a call to the ``read`` method of the ``res.users`` model:

        >>> data = odoo.json(
        ...     '/web/dataset/call',
        ...     {'model': 'res.users', 'method': 'read',
        ...      'args': [[1], ['name']]})
        >>> from pprint import pprint
        >>> pprint(data)
        {'id': ...,
         'jsonrpc': '2.0',
         'result': [{'id': 1, 'name': 'Administrator'}]}

        *Python 2:*

        :return: a dictionary (JSON response)
        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib2.HTTPError` (if `params` is not a dictionary)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: a dictionary (JSON response)
        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib.error.HTTPError` (if `params` is not a dictionary)
        :raise: `urllib.error.URLError` (connection error)
        """
        data = self._connector.proxy_json(url, params)
        if data.get('error'):
            raise error.RPCError(
                data['error']['data']['message'],
                data['error'])
        return data

    def http(self, url, data, headers=None):
        """Low level method to execute raw HTPP queries.

        .. note::

            For low level JSON-RPC queries, see the more convenient
            :func:`odoorpc.ODOO.json` method instead.

        You have to know the names of each POST parameter required by the
        URL, and set them in the `data` string/buffer.
        The `data` argument must be built by yourself, following the expected
        URL parameters (with :func:`urllib.urlencode` function for simple
        parameters, or multipart/form-data structure to handle file upload).

        E.g., the HTTP raw query to backup a database on `Odoo 8.0`:

        .. doctest::
            :options: +SKIP

            >>> response = odoo.http(
            ...     'web/database/backup',
            ...     'token=foo&backup_pwd=admin&backup_db=db_name')
            >>> binary_data = response.read()

        .. doctest::
            :hide:

            >>> response = odoo.http(
            ...     'web/database/backup',
            ...     'token=foo&backup_pwd=%s&backup_db=%s' % (SUPER_PWD, DB))
            >>> binary_data = response.read()

        *Python 2:*

        :return: `urllib.addinfourl`
        :raise: `urllib2.HTTPError`
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: `http.client.HTTPResponse`
        :raise: `urllib.error.HTTPError`
        :raise: `urllib.error.URLError` (connection error)
        """
        return self._connector.proxy_http(url, data, headers)

    # NOTE: in the past this function was implemented as a decorator for
    # methods needing to be checked, but Sphinx documentation generator is not
    # able to parse decorated methods.
    def _check_logged_user(self):
        """Check if a user is logged. Otherwise, an error is raised."""
        if not self._env or not self._password or not self._login:
            raise error.InternalError("Login required")

    def login(self, db, login='admin', password='admin'):
        """Log in as the given `user` with the password `passwd` on the
        database `db`.

        .. doctest::
            :options: +SKIP

            >>> odoo.login('db_name', 'admin', 'admin')
            >>> odoo.env.user.name
            'Administrator'

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib.error.URLError` (connection error)
        """
        # Get the user's ID and generate the corresponding user record
        data = self.json(
            '/web/session/authenticate',
            {'db': db, 'login': login, 'password': password})
        uid = data['result']['uid']
        if uid:
            context = data['result']['user_context']
            self._env = Environment(self, db, uid, context=context)
            self._login = login
            self._password = password
        else:
            raise error.RPCError("Wrong login ID or password")

    def logout(self):
        """Log out the user.

        >>> odoo.logout()
        True

        *Python 2:*

        :return: `True` if the operation succeed, `False` if no user was logged
        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: `True` if the operation succeed, `False` if no user was logged
        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib.error.URLError` (connection error)
        """
        if not self._env:
            return False
        self.json('/web/session/destroy', {})
        self._env = None
        self._login = None
        self._password = None
        return True

    # ------------------------- #
    # -- Raw XML-RPC methods -- #
    # ------------------------- #

    def execute(self, model, method, *args):
        """Execute the `method` of `model`.
        `*args` parameters varies according to the `method` used.

        .. doctest::
            :options: +SKIP

            >>> odoo.execute('res.partner', 'read', [1], ['name'])
            [{'id': 1, 'name': 'YourCompany'}]

        .. doctest::
            :hide:

            >>> data = odoo.execute('res.partner', 'read', [1], ['name'])
            >>> data[0]['id'] == 1
            True
            >>> data[0]['name'] == 'YourCompany'
            True

        *Python 2:*

        :return: the result returned by the `method` called
        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: the result returned by the `method` called
        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._check_logged_user()
        # Execute the query
        args_to_send = [self.env.db, self.env.uid, self._password,
                        model, method]
        args_to_send.extend(args)
        data = self.json(
            '/jsonrpc',
            {'service': 'object',
             'method': 'execute',
             'args': args_to_send})
        return data['result']

    def execute_kw(self, model, method, args=None, kwargs=None):
        """Execute the `method` of `model`.
        `args` is a list of parameters (in the right order),
        and `kwargs` a dictionary (named parameters). Both varies according
        to the `method` used.

        .. doctest::
            :options: +SKIP

            >>> odoo.execute_kw('res.partner', 'read', [[1]], {'fields': ['name']})
            [{'id': 1, 'name': 'YourCompany'}]

        .. doctest::
            :hide:

            >>> data = odoo.execute_kw('res.partner', 'read', [[1]], {'fields': ['name']})
            >>> data[0]['id'] == 1
            True
            >>> data[0]['name'] == 'YourCompany'
            True

        *Python 2:*

        :return: the result returned by the `method` called
        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: the result returned by the `method` called
        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._check_logged_user()
        # Execute the query
        args = args or []
        kwargs = kwargs or {}
        args_to_send = [self.env.db, self.env.uid, self._password,
                        model, method]
        args_to_send.extend([args, kwargs])
        data = self.json(
            '/jsonrpc',
            {'service': 'object',
             'method': 'execute_kw',
             'args': args_to_send})
        return data['result']

    def exec_workflow(self, model, record_id, signal):
        """Execute the workflow `signal` on
        the instance having the ID `record_id` of `model`.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._check_logged_user()
        # Execute the workflow query
        args_to_send = [self.env.db, self.env.uid, self._password,
                        model, signal, record_id]
        data = self.json(
            '/jsonrpc',
            {'service': 'object',
             'method': 'exec_workflow',
             'args': args_to_send})
        return data['result']

    # ---------------------- #
    # -- Session methods  -- #
    # ---------------------- #

    def save(self, name, rc_file='~/.odoorpcrc'):
        """Save the current :class:`ODOO <odoorpc.ODOO>` instance (a `session`)
        inside `rc_file` (``~/.odoorpcrc`` by default). This session will be
        identified by `name`::

            >>> import odoorpc
            >>> odoo = odoorpc.ODOO('localhost', port=8069)
            >>> odoo.login('db_name', 'admin', 'admin')
            >>> odoo.save('foo')

        Use the :func:`list <odoorpc.ODOO.list>` class method to list all
        stored sessions, and the :func:`load <odoorpc.ODOO.load>` class method
        to retrieve an already-connected :class:`ODOO <odoorpc.ODOO>` instance.

        *Python 2:*

        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `IOError`

        *Python 3:*

        :raise: :class:`odoorpc.error.InternalError` (if not logged)
        :raise: `PermissionError`
        :raise: `FileNotFoundError`
        """
        self._check_logged_user()
        data = {
            'type': self.__class__.__name__,
            'host': self.host,
            'protocol': self.protocol,
            'port': self.port,
            'timeout': self.config['timeout'],
            'user': self._login,
            'passwd': self._password,
            'database': self.env.db,
        }
        session.save(name, data, rc_file)

    @classmethod
    def load(cls, name, rc_file='~/.odoorpcrc'):
        """Return a connected :class:`ODOO` session identified by `name`:

        .. doctest::
            :options: +SKIP

            >>> import odoorpc
            >>> odoo = odoorpc.ODOO.load('foo')

        Such sessions are stored with the
        :func:`save <odoorpc.ODOO.save>` method.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError`
        :raise: `urllib.error.URLError` (connection error)
        """
        data = session.get(name, rc_file)
        if data.get('type') != cls.__name__:
            raise error.InternalError(
                "'{0}' session is not of type '{1}'".format(
                    name, cls.__name__))
        odoo = cls(
            host=data['host'],
            protocol=data['protocol'],
            port=data['port'],
            timeout=data['timeout'],
        )
        odoo.login(
            db=data['database'], login=data['user'], password=data['passwd'])
        return odoo

    @classmethod
    def list(cls, rc_file='~/.odoorpcrc'):
        """Return a list of all stored sessions available in the
        `rc_file` file:

        .. doctest::
            :options: +SKIP

            >>> import odoorpc
            >>> odoorpc.ODOO.list()
            ['foo', 'bar']

        Use the :func:`save <odoorpc.ODOO.save>` and
        :func:`load <odoorpc.ODOO.load>` methods to manage such sessions.

        *Python 2:*

        :raise: `IOError`

        *Python 3:*

        :raise: `PermissionError`
        :raise: `FileNotFoundError`
        """
        sessions = session.get_all(rc_file)
        return [name for name in sessions
                if sessions[name].get('type') == cls.__name__]
        #return session.list(rc_file)

    @classmethod
    def remove(cls, name, rc_file='~/.odoorpcrc'):
        """Remove the session identified by `name` from the `rc_file` file:

        .. doctest::
            :options: +SKIP

            >>> import odoorpc
            >>> odoorpc.ODOO.remove('foo')
            True

        *Python 2:*

        :raise: `ValueError` (if the session does not exist)
        :raise: `IOError`

        *Python 3:*

        :raise: `ValueError` (if the session does not exist)
        :raise: `PermissionError`
        :raise: `FileNotFoundError`
        """
        data = session.get(name, rc_file)
        if data.get('type') != cls.__name__:
            raise error.InternalError(
                "'{0}' session is not of type '{1}'".format(
                    name, cls.__name__))
        return session.remove(name, rc_file)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
