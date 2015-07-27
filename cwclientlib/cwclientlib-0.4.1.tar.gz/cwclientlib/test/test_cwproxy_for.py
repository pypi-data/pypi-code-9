# -*- coding: utf-8 -*-
#
# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
import tempfile
from unittest import TestCase
import json
import yaml
from contextlib import contextmanager

from cwclientlib import cwproxy_for

__docformat__ = "restructuredtext en"


CFG = {'sr ok':
       {'url': 'http://www.cubicweb.org',
        'auth-mech': 'signedrequest',
        'token-id': 'toto',
        'secret': 'mysecret',
        },
       'sr2 ok':
       {'url': 'http://www.cubicweb.org',
        'token-id': 'toto',
        'secret': 'mysecret',
        },
       'sr err':
       {'token-id': 'toto',
        'secret': 'mysecret',
        },
       'sr2 err':
       {'url': 'http://www.cubicweb.org',
        'secret': 'mysecret',
        },
       'sr3 err':
       {'url': 'http://www.cubicweb.org',
        'token-id': 'toto',
        },
       'kerb ok':
       {'url': 'http://www.cubicweb.org',
        'auth-mech': 'kerberos',
        },
       'auth-mech err':
       {'url': 'http://www.cubicweb.org',
        'auth-mech': 'other mech',
        },
       }


def cfg2ini(cfg):
    cfg = ('[%s]\n%s' % (s, ''.join('%s = %s\n' % (k, v)
                                    for k, v in sval.items()))
           for s, sval in cfg.items())
    return '\n'.join(cfg)


class CWProxyForTC(TestCase):
    '''Basic tests for CWProxy'''

    @contextmanager
    def temp_config_file(self, suffix='rc', mode=0o600):
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            if suffix == '.json':
                f.write(json.dumps(CFG).encode('utf-8'))
            elif suffix == '.yaml':
                f.write(yaml.dump(CFG, default_flow_style=False)
                        .encode('utf-8'))
            else:
                f.write(cfg2ini(CFG).encode('utf-8'))
        os.chmod(f.name, mode)
        os.environ['CWCLCONF'] = f.name
        try:
            yield
        finally:
            os.remove(f.name)

    def test_signedrequest_ini(self):
        with self.temp_config_file():
            for src in CFG:
                if src.endswith('ok'):
                    self.assertTrue(cwproxy_for(src))
                else:
                    with self.assertRaises(ValueError) as cm:
                        cwproxy_for(src)

    def test_signedrequest_json(self):
        with self.temp_config_file(suffix='.json'):
            for src in CFG:
                if src.endswith('ok'):
                    self.assertTrue(cwproxy_for(src))
                else:
                    with self.assertRaises(ValueError) as cm:
                        cwproxy_for(src)

    def test_signedrequest_yaml(self):
        with self.temp_config_file(suffix='.yaml'):
            for src in CFG:
                if src.endswith('ok'):
                    self.assertTrue(cwproxy_for(src))
                else:
                    with self.assertRaises(ValueError) as cm:
                        cwproxy_for(src)

    def test_signedrequest_configfile_permissions(self):
        src = 'sr ok'

        for mode in (0o400, 0o600):
            with self.temp_config_file(mode=mode):
                self.assertTrue(cwproxy_for(src))

        for mode in (0o700, 0o640, 0o604):
            with self.temp_config_file(mode=0o700):
                with self.assertRaises(EnvironmentError) as cm:
                    cwproxy_for(src)

if __name__ == '__main__':
    from unittest import main
    main()
