# Copyright 2012 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://launchpad.net/launcherposta

"""Interface for program data in disk."""

import copy_reg
import logging
import os
import pickle
import tempfile
import UserDict

# stupid gtk3; pylint: disable=E0611
from gi.repository import GdkPixbuf
# stupid gtk3; pylint: enable=E0611


def _pixbuf_reducer_load(imgbytes):
    """Helper for pickle to load a pixbuf."""
    # save bytes to a file
    fd, fpath = tempfile.mkstemp()
    fh = os.fdopen(fd, 'wb')
    fh.write(imgbytes)
    fh.close()

    # load pixbuf from the file, and remove it
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(fpath)
    os.unlink(fpath)
    return pixbuf


def _pixbuf_reducer_save(obj):
    """Helper for pickle to save a pixbuf."""
    # export pixbuf to a file
    fd, fpath = tempfile.mkstemp()
    obj.savev(fpath, 'png', [], [])

    # load bytes from the file, and remove it
    with open(fpath, 'rb') as fh:
        imgbytes = fh.read()
    os.close(fd)
    os.unlink(fpath)
    return (_pixbuf_reducer_load, (imgbytes,))

copy_reg.pickle(GdkPixbuf.Pixbuf, _pixbuf_reducer_save)


class ProgramData(UserDict.DictMixin):
    """Holder / interface for program data."""

    # more recent version of the in-disk data
    last_programs_version = 1

    def __init__(self, filename):
        self.filename = filename
        self.logger = logging.getLogger("ProgramData")
        self.logger.info("Using data file: %r", filename)

        self.version = None
        self.data = None
        self.load()
        if self.version != self.last_programs_version:
            raise ValueError("Unsupported data version: %r" % (self.version,))

    def load(self):
        """Load the data from the file."""
        # if not file, all empty
        if not os.path.exists(self.filename):
            self.data = {}
            self.version = self.last_programs_version
            return

        # get from the file
        with open(self.filename, 'rb') as fh:
            self.version, self.data = pickle.load(fh)

    def __str__(self):
        return "<ProgramsData ver=%r len=%d>" % (self.version, len(self.data))

    def __getitem__(self, pos):
        return self.data[pos]

    def __setitem__(self, pos, value):
        self.data[pos] = value

    def keys(self):
        """Return the keys of data."""
        return self.data.keys()

    def save(self):
        """Save to disk."""
        to_save = (self.last_programs_version, self.data)
        with open(self.filename, 'wb') as fh:
            pickle.dump(to_save, fh)
