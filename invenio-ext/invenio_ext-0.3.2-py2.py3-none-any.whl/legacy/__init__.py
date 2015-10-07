# -*- coding: utf-8 -*-
# This file is part of Invenio.
# Copyright (C) 2011, 2012, 2013, 2014, 2015 CERN.
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

"""Tools for working with legacy application."""

from __future__ import print_function

import os

import sys

from flask import abort, current_app, render_template, send_from_directory

from invenio_base import signals
from invenio_base.scripts.database import create, recreate
from invenio_base.utils import run_py_func

from .request_class import LegacyRequest


def cli_cmd_reset(sender, yes_i_know=False, drop=True, **kwargs):
    """Reset legacy values."""
    cmds = []
    if 'invenio_access' in current_app.config['PACKAGES']:
        from invenio_access.scripts.webaccessadmin import main as \
            webaccessadmin
        cmds.append(
            (webaccessadmin, "webaccessadmin -u admin -c -a -D")
        )

    for cmd in cmds:
        if run_py_func(*cmd, passthrough=True).exit_code:
            print("ERROR: failed execution of", *cmd)
            sys.exit(1)

signals.post_command.connect(cli_cmd_reset, sender=create)
signals.post_command.connect(cli_cmd_reset, sender=recreate)


def setup_app(app):
    """Setup up the app."""
    # Legacy config support
    _use_x_sendfile = app.config.get('CFG_BIBDOCFILE_USE_XSENDFILE')
    _debug = app.config.get('CFG_DEVEL_SITE', 0) > 0
    app.config.setdefault('USE_X_SENDFILE', _use_x_sendfile)
    app.config.setdefault('DEBUG', _debug)
    app.debug = app.config['DEBUG']

    # Legacy directory that must exist
    for cfg_dir in ['CFG_BATCHUPLOADER_DAEMON_DIR',
                    'CFG_BIBDOCFILE_FILEDIR',
                    'CFG_BIBENCODE_DAEMON_DIR_NEWJOBS',
                    'CFG_BIBENCODE_DAEMON_DIR_OLDJOBS',
                    'CFG_BIBENCODE_TARGET_DIRECTORY',
                    'CFG_BINDIR',
                    'CFG_CACHEDIR',
                    'CFG_ETCDIR',
                    'CFG_LOCALEDIR',
                    'CFG_LOGDIR',
                    'CFG_PYLIBDIR',
                    'CFG_RUNDIR',
                    'CFG_TMPDIR',
                    'CFG_TMPSHAREDDIR',
                    'CFG_WEBBASKET_DIRECTORY_BOX_NUMBER_OF_COLUMNS',
                    'CFG_WEBDIR',
                    'CFG_WEBSUBMIT_BIBCONVERTCONFIGDIR',
                    'CFG_WEBSUBMIT_COUNTERSDIR',
                    'CFG_WEBSUBMIT_STORAGEDIR']:
        path = app.config.get(cfg_dir)
        if path:
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            except OSError:
                app.logger.exception("Cannot property create directory {path} "
                                     "for legacy variable {cfg_dir}"
                                     .format(path=path, cfg_dir=cfg_dir))

    # Set custom request class.
    app.request_class = LegacyRequest

    @app.errorhandler(404)
    @app.errorhandler(405)
    def page_not_found(error):
        if error.code == 404:
            return render_template('404.html'), 404
        return str(error), error.code

    @app.route('/admin/<module>/<action>.py', methods=['GET', 'POST', 'PUT'])
    @app.route('/admin/<module>/<action>.py/<path:arguments>',
               methods=['GET', 'POST', 'PUT'])
    def web_admin(module, action, arguments=None):
        """Add support for legacy mod publisher."""
        return render_template('404.html'), 404

    @app.endpoint('static')
    def static_handler_with_legacy_publisher(*args, **kwargs):
        """Serve static files from instance path."""
        # Static file serving for devserver
        # ---------------------------------
        # Apache normally serve all static files, but if we are using the
        # devserver we need to serve static files here.
        filename = kwargs.get("filename")
        if not app.config.get('CFG_FLASK_SERVE_STATIC_FILES') \
                or filename is None or app.static_folder is None:
            abort(404)
        else:
            return send_from_directory(app.static_folder, filename)

    return app
