# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, unicode_literals, division

import os
from glob import glob
from pkg_resources import resource_string

from cffi import FFI
from distutils.sysconfig import get_python_lib  # pylint: disable=F0401

from .compat import PYPY


__all__ = (
    'libnahpack',
)


_header = resource_string('nahpackpy', 'nahpack.h').decode('utf8')


ffi = FFI()


ffi.cdef(_header)
if not PYPY:  # pragma: no cover
    ffi.cdef('void initnahpack(void);')  # assumed by CPython


_site_packages_path = get_python_lib()
_so_path = glob(os.path.join(_site_packages_path, 'nahpack*.so'))[0]


libnahpack = ffi.dlopen(os.path.join(_site_packages_path, _so_path))
