# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
#               2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Helper functions for building and running test suites."""

from __future__ import print_function, with_statement

import StringIO
import binascii
import unittest

from flask import url_for, current_app
from flask_testing import TestCase
from invenio_ext.sqlalchemy import db
from invenio_ext.sqlalchemy.utils import session_manager
from six import iteritems

from .version import __version__

CFG_TESTUTILS_VERBOSE = 1

nottest = unittest.skip('nottest')


class InvenioTestCase(TestCase):

    """Base test case for invenio."""

    @property
    def config(self):
        """Configuration property."""
        cfg = {
            'engine': 'CFG_DATABASE_TYPE',
            'host': 'CFG_DATABASE_HOST',
            'port': 'CFG_DATABASE_PORT',
            'username': 'CFG_DATABASE_USER',
            'password': 'CFG_DATABASE_PASS',
            'database': 'CFG_DATABASE_NAME',
        }
        out = {}
        for (k, v) in iteritems(cfg):
            if hasattr(self, k):
                out[v] = getattr(self, k)
        return out

    def create_app(self):
        """Create the Flask application for testing."""
        from invenio_base.factory import create_app
        app = create_app(**self.config)
        app.testing = True
        return app

    def login(self, username, password):
        """Log in as username and password."""
        return self.client.post(
            url_for('webaccount.login'),
            base_url=current_app.config['CFG_SITE_SECURE_URL'],
            data=dict(nickname=username,
                      password=password),
            follow_redirects=True)

    def logout(self):
        """Log out."""
        return self.client.get(
            url_for('webaccount.logout'),
            base_url=current_app.config['CFG_SITE_SECURE_URL'],
            follow_redirects=True)

    def shortDescription(self):
        """Return a short description of the test case."""
        return

    @session_manager
    def delete_objects(self, list_of_objects):
        """Delete a list of objects from the database.

        :param list_of_objects: list of objects to delete
        """
        for obj in list_of_objects:
            db.session.delete(obj)

    @session_manager
    def create_objects(self, list_of_objects):
        """Create a list of new objects into the database.

        :param list_of_objects: list of objects to create
        """
        for obj in list_of_objects:
            db.session.add(obj)


def base64_to_file(base64_file, filepath):
    """Write a base64 encoded version of a file to disk."""
    with open(filepath, 'wb') as f:
        f.write(binascii.a2b_base64(base64_file))


def file_to_base64(filepath):
    """Get base64 encoded version of a file.

    Useful to encode a test file for inclusion in tests.
    """
    with open(filepath, 'rb') as f:
        return binascii.b2a_base64(f.read())


def stringio_to_base64(stringio_obj):
    """Get base64 encoded version of a StringIO object."""
    return binascii.b2a_base64(stringio_obj.getvalue())


def make_file_fixture(filename, base64_file):
    """
    Generate a file fixture suitable for use with the Flask test client.

    :param base64_file: A string encoding a file in base64. Use
        file_to_base64() to get the base64 encoding of a file. If not provided
        a PDF file be generated instead, including
    """
    fp = StringIO.StringIO(binascii.a2b_base64(base64_file))
    return fp, filename


def make_pdf_fixture(filename, text=None):
    """
    Generate a PDF fixture.

    It's suitable for use with Werkzeug test client and Flask test request
    context.

    Use of this function requires that reportlab have been installed.

    :param filename: Desired filename.
    :param text: Text to include in PDF. Defaults to "Filename: <filename>", if
        not specified.
    """
    if text is None:
        text = "Filename: %s" % filename

    # Generate simple PDF
    from reportlab.pdfgen import canvas
    output = StringIO.StringIO()
    c = canvas.Canvas(output)
    c.drawString(100, 100, text)
    c.showPage()
    c.save()

    return make_file_fixture(filename, stringio_to_base64(output))
