# -*- coding: utf-8 -*-
#
# File: defaults.py
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'

import os
import sys
import logging
import textwrap
import ConfigParser

__all__ = ["get_defaults"]

logger = logging.getLogger("nexiles.tools.api")


def get_default_config_content():
    return textwrap.dedent("""
    [nxtools]
    ; These settings are for all commands.
    ; -----------------------------------------------------

    ; Verbosity.  Set to `true` for more output
    verbose=false

    ; to enable logging to a file set this to a path
    ; logfile=nxtools.log

    ; logging level.  debug|info|warning|error
    loglevel = info

    ; to enter the post-mortem debugger on exceptions
    ; set this to true
    post-mortem = false

    ; The default Windchill URL
    ; default-url=https://skynet.nexiles.com/Windchill

    ; The default `type` for queries
    ; default-type=documents


    [apps]
    ; These settings are for app development
    ; -----------------------------------------------------
    ;
    ; Note: These are defaults which can be overwritten by
    ;       command line switches

    ; the name of the app template for the 'app-create' command
    app-template=template

    ; The name of a Windchill context to store apps to.
    app-container-name=nxDemo

    ; The path to a folder where apps are stored.
    ; app-folder-path=/Default/apps

    ; The default "start page" of apps.
    ; Note: This is **only** used in the `app-open` command
    ; app-start-page=index.html

    ; Which directory in the root of an app development directory
    ; contains the "public" app files?
    ; app-source-dir=static
    """)


def get_default_config_path():
    if sys.platform.startswith("win"):
        return os.path.normpath(os.path.expanduser("~/_nxtools/default.ini"))
    else:
        return os.path.expanduser("~/.nxtools/default.ini")


def make_default_config():
    path = get_default_config_path()
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)

    print "No default configuration found!"
    print "Createing the following default configuration in : ", path
    print get_default_config_content()

    with file(path, "w") as f:
        f.write(get_default_config_content())

    return path


class Configuration(object):
    def __init__(self, path):
        self.base_section = "nxtools"
        self.path = path
        self.parser = ConfigParser.SafeConfigParser()
        if path and os.path.exists(path):
            self.parser.read(path)

    def from_string(self, s):
        import StringIO
        io = StringIO.StringIO(s)
        self.parser.readfp(io)
        return self

    def get(self, key, default=None, section=None):
        if section is None:
            section = self.base_section

        try:
            return self.parser.get(section, key)
        except ConfigParser.NoOptionError:
            return default

    def get_bool(self, key, default=False):
        s = self.get(key, default and "yes" or "no").lower()
        if s in ("yes", "true", "1", "on"):
            return True
        return False


class Defaults(Configuration):

    def __init__(self, path=None):
        if path is None:
            path = get_default_config_path()
            if not os.path.exists(path):
                path = make_default_config()
        super(Defaults, self).__init__(path)

    def get_default_url(self):
        return self.get("default-url", "https://skynet.nexiles.com/Windchill")

    def get_default_type(self):
        return self.get("default-type", "document")

    def get_loglevel(self):
        l = self.get("loglevel", None).upper()
        if l is None:
            # XXX: maybe use os.environ["NXTOOL_LOGLEVEL]
            return logging.INFO

        if l in ("INFO", "DEBUG", "ERROR", "WARNING"):
            l = getattr(logging, l)
            return l
        return logging.INFO

    @property
    def wt_username(self):
        return os.environ.get("WTUSER")

    @property
    def wt_pass(self):
        return os.environ.get("WTPASS")

    @property
    def default_url(self):
        return self.get_default_url()

    @property
    def default_type(self):
        return self.get_default_type()

    @property
    def verbose(self):
        return self.get_bool("verbose")

    @property
    def post_mortem(self):
        return self.get_bool("post-mortem")

    @property
    def loglevel(self):
        return self.get_loglevel()

    @property
    def logfile(self):
        return self.get("logfile", None)

    @property
    def app_template_name(self):
        return self.get("app-template-name", section="apps", default="template")

    @property
    def app_container_name(self):
        return self.get("app-container-name", section="apps", default="TestProduct")

    @property
    def app_folder_path(self):
        return self.get("app-folder-path", section="apps", default="/Default/apps")

    @property
    def app_start_page(self):
        return self.get("app-start-page", section="apps", default="index.html")

    @property
    def app_source_dir(self):
        return self.get("app-source-dir", section="apps", default="static")


def get_defaults(path=None):
    return Defaults(path)

# vim: set ft=python ts=4 sw=4 expandtab :
