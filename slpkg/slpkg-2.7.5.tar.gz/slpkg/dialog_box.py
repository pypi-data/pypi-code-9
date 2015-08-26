#! /usr/bin/python
# -*- coding: utf-8 -*-

# dialog_box.py file is part of slpkg.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals


class DialogUtil(object):
    """Create dialog checklist
    """
    def __init__(self, data, text, title, backtitle, status):
        try:
            from dialog import Dialog
        except ImportError:
            print("Require 'pythondialog': Install with '# slpkg -s sbo "
                  "python2-pythondialog'")
            raise SystemExit()
        self.d = Dialog(dialog="dialog", autowidgetsize=True)
        self.data = data
        self.text = text
        self.title = title
        self.backtitle = backtitle
        self.status = status
        self.ununicode = []
        self.tags = []

    def checklist(self):
        """Run dialog checklist
        """
        try:
            choice = []
            for item in self.data:
                choice.append((item, "", self.status))
            code, self.tags = self.d.checklist(
                text=self.text, height=20, width=65, list_height=13,
                choices=choice, title=self.title, backtitle=self.backtitle)
        except KeyboardInterrupt:
            print("")
            raise SystemExit()
        if code == "ok":
            self.ununicode_to_string()
            return self.ununicode
        if code == "cancel":
            self.exit()

    def exit(self):
        """Exit from dialog
        """
        raise SystemExit()

    def ununicode_to_string(self):
        """Convert unicode in string
        """
        for tag in self.tags:
            self.ununicode.append(str(tag))
