# -*- coding: utf-8 -*-
#
# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cwclientlib. If not, see <http://www.gnu.org/licenses/>.

import os

from .cwproxy import CWProxy, SignedRequestAuth


def cwproxy_for(instance, **kw):
    """Build a CWProxy instance for a given cubicweb instance, reading
    authentication credentials from a ini, a json config file or a
    YAML file.

    :param instance: can be either the name of the instance in the config
    file, or its URL

    :param **kw: will be passed to the proxy class constructor; the
    instanciated proxy class can be specified as a proxycls named
    argument

    The config file is ~/.config/cwclientlibrc by default (ini
    format), but this can be changed by setting the CWCLCONF
    environment variable (the ~/.config can be overriden by the
    XDG_CONFIG_HOME env var, see
    http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html).

    By default, the configuration format is the ini file format ; it
    must look like:

      [cwo]
      url = https://www.cubicweb.org/
      token-id = my token id
      secret = <my secret>

      [intra]
      url = https://my.intranet
      auth-mech = kerberos
      server-ca = /path/to/ca-bundle.pem
      kerberos-mutual-auth = disabled

    If the file name ends with .json, it will be read by a JSON
    parser, like:

      {'cwo': {'url': 'https://www.cubicweb.org/',
               'token-id': 'my token id',
               'secret': '<my secret>'},
       'intra': {'url': 'https://my.intranet',
                 'auth-mech': 'kerberos',
                 'kerberos-mutual-auth': 'disabled',
                 'server-ca': '/path/to/ca-bundle.pem',},
      }

    If the file name ends with .yaml, it will be read by a YAML
    parser, like:

      cwo:
        url: https://www.cubicweb.org/
        token-id: my token id
        secret: <my secret>
      intra:
        url: https://my.intranet
        auth-mech: kerberos
        kerberos-mutual-auth: disabled
        server-ca: /path/to/ca-bundle.pem

    Supported authentications are 'signedrequest' and 'kerberos'. The
    default authentication mechanism is 'signedrequest'

    When using kerberos authentication, the 'kerberos-mutual-auth' config
    option may be set to 'disabled', 'optional' or 'required'.

    """
    cfg = get_config()
    # if instance is not the id of a cw endpoint, loop in config
    # entries to match on url
    if instance not in cfg:
        instances = [inst for inst, instcfg in cfg.items()
                     if instance.startswith(instcfg.get('url'))]
        if len(instances) == 1:
            instance = instances[0]
    if instance not in cfg:
        raise ValueError('Cannot find a configuration entry for %r' % instance)

    cfg = cfg[instance]
    auth_mech = cfg.get('auth-mech', 'signedrequest')
    url = cfg.get('url')
    if not url:
        raise ValueError('Missing "url" configuration option')

    if auth_mech == 'signedrequest':
        tokenid = cfg.get('token-id')
        secret = cfg.get('secret')
        if not tokenid or not secret:
            raise ValueError('Missing "token-id" or "secret" configuration '
                             'option for signedrequest')
        auth = SignedRequestAuth(tokenid, secret)

    elif auth_mech == 'kerberos':
        from requests_kerberos import (HTTPKerberosAuth,
                                       DISABLED, OPTIONAL, REQUIRED)
        mmap = {'disabled': DISABLED,
                'optional': OPTIONAL,
                'required': REQUIRED}
        mutual = mmap.get(cfg.get('kerberos-mutual-auth', 'optional'))
        if mutual is None:
            raise ValueError('Unknown kerberos-mutual-auth config option: '
                             '%r' % cfg.get('kerberos-mutual-auth'))
        auth = HTTPKerberosAuth(mutual_authentication=mutual)
    else:
        raise ValueError('Unknown authentication mechanism (auth-mech): '
                         '%r' % auth_mech)
    if 'server-ca' in cfg:
        kw['verify'] = cfg['server-ca']

    proxy_cls = kw.pop('proxycls', CWProxy)
    return proxy_cls(url, auth, **kw)


def get_config():
    defaultcfg = os.path.join(os.environ.get('XDG_CONFIG_HOME', '~/.config'),
                              'cwclientlibrc')
    cfgfile = os.path.expanduser(os.environ.get('CWCLCONF', defaultcfg))
    if not os.path.isfile(cfgfile):
        raise EnvironmentError('Cannot find the configuration file %r' %
                               cfgfile)
    perms = os.stat(cfgfile).st_mode % (0o1000)
    if (perms & 0o600) != perms:
        raise EnvironmentError("%r permissions should be 0600 or 0400 (%o)" %
                               (cfgfile, perms))

    if cfgfile.endswith('.json'):
        import json
        with open(cfgfile) as f:
            cfg = json.load(f)
    elif cfgfile.endswith('.yaml'):
        import yaml
        with open(cfgfile) as f:
            cfg = yaml.load(f)
    else:
        from six.moves import configparser as cp
        cp = cp.ConfigParser()
        cp.read(cfgfile)
        cfg = {section: dict(cp.items(section)) for section in cp.sections()}
    return cfg
