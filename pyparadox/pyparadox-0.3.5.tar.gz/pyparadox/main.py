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
import logging
import logging.config
import json
from pkg_resources import resource_filename

import appdirs

from .config import default_values, FileConfig, DEFAULT_CONFIG_DIR
from .core import GAMES, make_command, execute_command
from . import __version__

_logger = logging.getLogger(__name__)


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

    _logger.info("loading config file from {}".format(path))
    config = FileConfig.build_config(path, default=default_values(game))

    from PyQt5 import QtWidgets
    from .gui import MainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName("PyParadox")

    _logger.debug("creating MainWindow")
    form = MainWindow(config)
    form.show()

    _logger.debug("starting Qt exec loop")
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
    if args == sys.argv:
        args = args[1:]
    parser = argparse.ArgumentParser(description="Launcher for Paradox titles")
    parser.add_argument("game", type=str, choices=list(GAMES.keys()),
                        help="Game to launch")
    parser.add_argument("-v", "--verbose", action="store_const",
                        dest="loglevel", const=logging.INFO)
    parser.add_argument("-d", "--debug", action="store_const", dest="loglevel",
                        const=logging.DEBUG)
    parser.add_argument("steam-command", nargs="?", help=argparse.SUPPRESS)

    result_args = parser.parse_args(args)

    with open(resource_filename("pyparadox", "resources/logging.json")) as fp:
        config = json.load(fp)

    default_level = config["handlers"]["console"]["level"]
    config["handlers"]["console"]["level"] = (result_args.loglevel if
                                              result_args.loglevel else
                                              default_level)

    log_dir = appdirs.user_data_dir("PyParadox")
    try:
        os.makedirs(log_dir)
    except FileExistsError:
        pass

    default_file = config["handlers"]["info_file_handler"]["filename"]
    config["handlers"]["info_file_handler"]["filename"] = \
        os.path.join(log_dir, default_file)

    logging.config.dictConfig(config)

    return result_args


if __name__ == "__main__":
    main()
