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

"""Main program."""

import json
import logging
import os
import subprocess
import time

# stupid gtk3; pylint: disable=E0611
from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator
# stupid gtk3; pylint: enable=E0611
from xdg import BaseDirectory

from launcherposta import widgets, pdata

# generic logger
logger = logging.getLogger()

BASEDIR = os.path.dirname(__file__)

RETURN_MESSAGES = {
      1: "Some miscellaneous error",
      2: "Misuse of shell builtins",
    126: "Command invoked cannot execute",
    127: "Command not found",
    128: "Invalid argument to exit",
    130: "Script terminated by Control-C",
}


def _should_fix(progname):
    """Tell if we should fix the Unity panel systray settings.

    Return None if don't need, else return the current conf.
    """
    cmd = "gsettings get com.canonical.Unity.Panel systray-whitelist".split()
    try:
        out = subprocess.check_output(cmd)
    except Exception, err:
        # don't have gsettings, nothing to fix
        etype = err.__class__.__name__
        logger.debug("No gsettings, no systray conf to fix (got %r %s)",
                     etype, err)
        return

    try:
        conf = map(str, json.loads(out.strip().replace("'", '"')))
    except ValueError:
        # don't understand the output, can't really fix it :/
        logger.warning("Don't understand gsettings output: %r", out)
        return

    logger.info("gsettings conf: %r", conf)
    if "all" in conf or progname in conf:
        # we're ok!
        return

    # need to fix
    return conf


def _fix_unity_systray(progname):
    """Check settings."""
    conf = _should_fix(progname)
    if conf is None:
        return

    conf.append(progname)
    cmd = ["gsettings", "set", "com.canonical.Unity.Panel",
           "systray-whitelist", str(conf)]
    try:
        out = subprocess.check_output(cmd)
    except OSError, err:
        logger.warning("Error trying to set the new conf: %s", err)
    else:
        logger.warning("New config set (result: %r)", out)


class Indicator(object):
    """The indicator."""
    def __init__(self, config, version):
        self.config = config
        self.version = version
        self.logger = logging.getLogger("Indicator")
        category = appindicator.IndicatorCategory.APPLICATION_STATUS
        icon_name = "launcherposta"
        logos_path = os.path.join(BASEDIR, 'logos')
        ind = appindicator.Indicator.new("launcherposta", icon_name, category)
        ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        ind.set_title("Launcher Posta")
        ind.set_icon_theme_path(logos_path)
        ind.set_icon(icon_name)
        self.indicator = ind
        self.menu = None
        self.set_menu()

    def set_menu(self):
        """Set the menu in the indicator."""
        menu = self._build_menu()
        self.indicator.set_menu(menu)

    def _build_menu(self):
        """Build the menu according to the config."""
        menu = Gtk.Menu()

        for appicon, appname, appcmd in self.config.get('menudata', []):
            self.logger.info("Building menu: %r", appname)
            item = Gtk.ImageMenuItem(appname)
            item.set_always_show_image(True)
            if appicon is not None:
                img = Gtk.Image.new_from_pixbuf(appicon)
                item.set_image(img)
            menu.append(item)
            item.connect("activate", self._execute, appcmd)
            item.show()

        self.logger.info("Building menu: the rest")
        accgroup = Gtk.AccelGroup()

        # separator
        item = Gtk.SeparatorMenuItem()
        menu.append(item)
        item.show()

        # edit
        item = Gtk.ImageMenuItem.new_from_stock("gtk-edit", accgroup)
        menu.append(item)
        item.connect("activate", self._edit_menu)
        item.show()

        # about
        item = Gtk.ImageMenuItem.new_from_stock("gtk-about", accgroup)
        menu.append(item)
        item.connect("activate", self._run_about_dialog)
        item.show()

        # quit!
        item = Gtk.ImageMenuItem.new_from_stock("gtk-quit", accgroup)
        menu.append(item)
        item.connect("activate", lambda *a: Gtk.main_quit())
        item.show()

        return menu

    def _edit_menu(self, _):
        """Edit the menu."""
        def apply_changes(new_data):
            """Apply the changes to real menu."""
            self.logger.info("Applying new menu items: %s", new_data)
            self.config['menudata'] = new_data
            self.config.save()
            self.set_menu()

        menudata = self.config.get('menudata', [])[:]
        widgets.ConfigWindow(menudata, apply_changes)

    def _execute(self, _, cmd):
        """Execute a cmd."""
        self.logger.info("Executing: %r", cmd)
        try:
            p = subprocess.Popen(cmd, shell=True)
        except OSError, err:
            self.logger.error("Execution failed: %s", err)
            widgets.show_error_dialog("Execution failed: " + str(err))
        else:
            # wait for the shell to execute and give it time to finish by
            # error if it had a problem; note that this sleep time does
            # not affect at all the GUI interaction
            time.sleep(1)

            # the poll is needed for the returncode to be set
            p.poll()

            if p.returncode is None or p.returncode == 0:
                self.logger.info("Execution ok, pid=%d", p.pid)
            else:
                returnmsg = RETURN_MESSAGES.get(p.returncode, p.returncode)
                self.logger.error("Execution failed, child returned %r (%s)",
                                  p.returncode, returnmsg)
                m = "Execution failed, child returned %r (%r)" % (returnmsg,
                                                                  p.returncode)
                widgets.show_error_dialog(m)

    def _run_about_dialog(self, _):
        """Run the About dialog."""
        dialog = widgets.get_about_dialog(self.version)
        dialog.run()
        dialog.hide()


def go(version):
    """Start it all."""
    GObject.threads_init()
    logger.info("Starting")
    config_filename = os.path.join(BaseDirectory.xdg_config_home,
                                   "launcherposta.conf")
    config = pdata.ProgramData(config_filename)
    Indicator(config, version)
    _fix_unity_systray("launcherposta")
    logger.info("Go!")
    Gtk.main()
