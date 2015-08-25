# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, unicode_literals, division

import sys


__all__ = (
    'PY3',
    'PYPY',
)


PY3 = sys.version_info >= (3, 0)

PYPY = hasattr(sys, 'pypy_version_info')
