# -*- coding: utf-8 -*-
#
# PyParadox is a nix launcher for Paradox titles.
# Copyright (C) 2014  Carmen Bianca Bakker <carmenbbakker@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
from pkg_resources import resource_filename

from .config import default_values, FileConfig, DEFAULT_CONFIG_DIR
from .core import GAMES, make_command, execute_command
from . import __version__


def main(game="ck2"):
    # main_console(["ck2"])
    main_gui([game])


def main_console(args=sys.argv):
    parser_args = _parse_args(args=args)
    game = parser_args.game
    path = os.path.join(DEFAULT_CONFIG_DIR, "pyparadox_{}.json".format(game))
    config = FileConfig.build_config(path, default=default_values(game))

    command = make_command(config["binary_path"],
                           config["excluded_dlcs"],
                           config["mods"])
    execute_command(command)


def main_gui(args=sys.argv):
    parser_args = _parse_args(args=args)
    game = parser_args.game
    path = os.path.join(DEFAULT_CONFIG_DIR, "pyparadox_{}.json".format(game))

    config = FileConfig.build_config(path, default=default_values(game))

    from PyQt5 import QtWidgets
    from .gui import MainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName("PyParadox")

    form = MainWindow(config)
    form.show()

    sys.exit(app.exec_())


def main_qml(args=sys.argv):
    parser_args = _parse_args(args=args)
    game = parser_args.game
    path = os.path.join(DEFAULT_CONFIG_DIR, "pyparadox_{}.json".format(game))

    config = FileConfig.build_config(path, default=default_values(game))

    from PyQt5 import QtCore, QtGui, QtWidgets, QtQml
    from .gui import PluginListModel, LogicWrapper

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName("PyParadox")

    engine = QtQml.QQmlApplicationEngine()

    rootContext = engine.rootContext()

    modsModel = PluginListModel()
    dlcsModel = PluginListModel()
    expansionsModel = PluginListModel()

    logicWrapper = LogicWrapper(config, modsModel, dlcsModel, expansionsModel)

    rootContext.setContextProperty("imagePath", resource_filename(
        "pyparadox",
        "resources/{}.png".format(game)))
    rootContext.setContextProperty("modsModel", modsModel)
    rootContext.setContextProperty("dlcsModel", dlcsModel)
    rootContext.setContextProperty("expansionsModel", expansionsModel)
    rootContext.setContextProperty("logicWrapper", logicWrapper)

    engine.load(QtCore.QUrl(resource_filename(
        "pyparadox",
        "resources/ui/main.qml")))
    window = engine.rootObjects()[0]
    window.setIcon(QtGui.QIcon(resource_filename(
        "pyparadox",
        "resources/paradox.png")))
    sys.exit(app.exec_())


def _parse_args(args=sys.argv):
    parser = argparse.ArgumentParser(description="Launcher for Paradox titles")
    parser.add_argument("game", type=str, choices=list(GAMES.keys()),
                        help="Game to launch")
    parser.add_argument("steam-command", nargs="?", help=argparse.SUPPRESS)
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()
