# Copyright (c) 2015 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

"""Unit tests for matching against authorized_keys file

   Note: These tests assume that the ssh-keygen command is available on
         the system and in the user's path.

"""

from asyncssh import import_public_key
#from asyncssh.auth_keys import read_authorized_keys

from .util import TempDirTestCase, run


class _TestAuthorizedKeys(TempDirTestCase):
    """Unit tests for auth_keys module"""

    keylist = []
    imported_keylist = []

    @classmethod
    def setUpClass(cls):
        """Create public keys needed for test"""

        super().setUpClass()

        for _ in range(3):
            run('ssh-keygen -t rsa -N "" -f key')

            with open('key.pub', 'r') as f:
                k = f.read()

            cls.keylist.append(k)
            cls.imported_keylist.append(import_public_key(k))

            run('rm key key.pub')

    def test_match(self):
        """Test authorized keys matching"""
