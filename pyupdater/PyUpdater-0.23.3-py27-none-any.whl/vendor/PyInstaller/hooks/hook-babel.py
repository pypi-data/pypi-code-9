#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from PyInstaller.hooks.hookutils import exec_statement

hiddenimports = ["babel.dates"]

babel_localedata_dir = exec_statement(
    "import babel.localedata; print babel.localedata._dirname")

datas = [
    (babel_localedata_dir, ""),
]
