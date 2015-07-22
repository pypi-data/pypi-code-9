#!/usr/bin/env python
# coding: utf-8
#
#    Project: FabIO tests class utilities
#             http://fable.sf.net
#
#
#    Copyright (C) 2010-2014 European Synchrotron Radiation Facility
#                       Grenoble, France
#
#    Principal authors: Jérôme KIEFFER (jerome.kieffer@esrf.fr)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the Lesser GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function, division, absolute_import, with_statement

__author__ = "Jérôme Kieffer"
__contact__ = "jerome.kieffer@esrf.eu"
__license__ = "LGPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "21/01/2015"

PACKAGE = "fabio"
SOURCES = PACKAGE + "-src"
DATA_KEY = "FABIO_DATA"

import os
import imp
import sys
import getpass
import subprocess
import threading
import distutils.util
import logging
import bz2
import gzip
import json
import tempfile


try:  # Python3
    from urllib.request import urlopen, ProxyHandler, build_opener
except ImportError:  # Python2
    from urllib2 import urlopen, ProxyHandler, build_opener
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("%s.utilstest" % PACKAGE)

TEST_HOME = os.path.dirname(os.path.abspath(__file__))
IN_SOURCES = SOURCES in os.listdir(os.path.dirname(TEST_HOME))

if IN_SOURCES:
    os.environ[DATA_KEY] = os.path.dirname(TEST_HOME)


class UtilsTest(object):
    """
    Static class providing useful stuff for preparing tests.
    """
    options = None
    timeout = 60  # timeout in seconds for downloading images
    url_base = "http://downloads.sourceforge.net/fable"
    sem = threading.Semaphore()
    recompiled = False
    reloaded = False
    name = PACKAGE

    if IN_SOURCES:
        image_home = os.path.join(os.path.dirname(TEST_HOME), "testimages")
        if not os.path.isdir(image_home):
            os.makedirs(image_home)
        testimages = os.path.join(TEST_HOME, "all_testimages.json")
        if os.path.exists(testimages):
            with open(testimages) as f:
                ALL_DOWNLOADED_FILES = set(json.load(f))
        else:
            ALL_DOWNLOADED_FILES = set()
        platform = distutils.util.get_platform()
        architecture = "lib.%s-%i.%i" % (platform,
                                         sys.version_info[0], sys.version_info[1])

        if os.environ.get("PYBUILD_NAME") == name:
            # we are in the debian packaging way
            home = os.environ.get("PYTHONPATH", "").split(os.pathsep)[-1]
        elif os.environ.get("BUILDPYTHONPATH"):
            home = os.path.abspath(os.environ.get("BUILDPYTHONPATH", ""))
        else:
            home = os.path.join(os.path.dirname(TEST_HOME),
                                      "build", architecture)
        logger.info("%s Home is: %s" % (name, home))
        if name in sys.modules:
            logger.info("%s module was already loaded from  %s" % (name, sys.modules[name]))
            fabio = None
            sys.modules.pop(name)
            for key in sys.modules.copy():
                if key.startswith(name + "."):
                    sys.modules.pop(key)

        if not os.path.isdir(home):
            with sem:
                if not os.path.isdir(home):
                    logger.warning("Building pyFAI to %s" % home)
                    p = subprocess.Popen([sys.executable, "setup.py", "build"],
                                         shell=False, cwd=os.path.dirname(TEST_HOME))
                    logger.info("subprocess ended with rc= %s" % p.wait())
                    recompiled = True
        logger.info("Loading %s" % name)
        try:
            fabio = imp.load_module(*((name,) + imp.find_module(name, [home])))
        except Exception as error:
            logger.warning("Unable to loading %s %s" % (name, error))
            if "-r" not in sys.argv:
                logger.warning("Remove build and start from scratch %s" % error)
                sys.argv.append("-r")
    else:
        try:
            fabio = __import__("%s.directories" % name)
            directories = fabio.directories
            image_home = directories.testimages
        except Exception as err:
            logger.warning("in loading directories %s", err)
            image_home = None
        if image_home is None:
            image_home = os.path.join(tempfile.gettempdir(), "%s_testimages_%s" % (name, getpass.getuser()))
            if not os.path.exists(image_home):
                os.makedirs(image_home)
        testimages = os.path.join(TEST_HOME, "all_testimages.json")
        if os.path.exists(testimages):
            with open(testimages) as f:
                ALL_DOWNLOADED_FILES = set(json.load(f))
        else:
            ALL_DOWNLOADED_FILES = set()
    tempdir = tempfile.mkdtemp("_" + getpass.getuser(), name + "_")

    @classmethod
    def deep_reload(cls):
        if not IN_SOURCES:
            cls.fabio = __import__(cls.name)
            return cls.fabio
        if cls.reloaded:
            return cls.fabio
        logger.info("Loading %s" % cls.name)
        cls.fabio = None
        fabio = None
        sys.path.insert(0, cls.home)
        for key in sys.modules.copy():
            if key.startswith(cls.name):
                sys.modules.pop(key)
        cls.fabio = __import__(cls.name)
        logger.info("%s loaded from %s" % (cls.name, cls.fabio.__file__))
        sys.modules[cls.name] = cls.fabio
        cls.reloaded = True
        return cls.fabio

    @classmethod
    def forceBuild(cls, remove_first=True):
        """
        force the recompilation of FabIO
        """
        if not IN_SOURCES:
            return
        if not cls.recompiled:
            with cls.sem:
                if not cls.recompiled:
                    logger.info("Building %s to %s" % (cls.name, cls.home))
                    if cls.name in sys.modules:
                        logger.info("%s module was already loaded from  %s" % (cls.name, sys.modules[cls.name]))
                        cls.fabio = None
                        sys.modules.pop(cls.name)
                    if remove_first:
                        recursive_delete(cls.home)
                    p = subprocess.Popen([sys.executable, "setup.py", "build"],
                                         shell=False, cwd=os.path.dirname(TEST_HOME))
                    logger.info("subprocess ended with rc= %s" % p.wait())
                    cls.fabio = cls.deep_reload()
                    cls.recompiled = True

    @classmethod
    def timeoutDuringDownload(cls, imagename=None):
            """
            Function called after a timeout in the download part ...
            just raise an Exception.
            """
            if imagename is None:
                imagename = "2252/testimages.tar.bz2 unzip it "
            raise RuntimeError("Could not automatically \
                download test images!\n \ If you are behind a firewall, \
                please set both environment variable http_proxy and https_proxy.\
                This even works under windows ! \n \
                Otherwise please try to download the images manually from \n %s/%s and put it in in test/testimages." % (cls.url_base, imagename))

    @classmethod
    def getimage(cls, imagename):
        """
        Downloads the requested image from Forge.EPN-campus.eu

        @param: name of the image.
        For the RedMine forge, the filename contains a directory name that is removed
        @return: full path of the locally saved file
        """
        cls.ALL_DOWNLOADED_FILES.add(imagename)
        try:
            with open(cls.testimages, "w") as fp:
                json.dump(list(cls.ALL_DOWNLOADED_FILES), fp, indent=4)
        except IOError:
            logger.debug("Unable to save JSON list")
        baseimage = os.path.basename(imagename)
        logger.info("UtilsTest.getimage('%s')" % baseimage)
        fullimagename = os.path.abspath(os.path.join(cls.image_home, baseimage))
        if not os.path.isfile(fullimagename):
            logger.info("Trying to download image %s, timeout set to %ss",
                        imagename, cls.timeout)
            dictProxies = {}
            if "http_proxy" in os.environ:
                dictProxies['http'] = os.environ["http_proxy"]
                dictProxies['https'] = os.environ["http_proxy"]
            if "https_proxy" in os.environ:
                dictProxies['https'] = os.environ["https_proxy"]
            if dictProxies:
                proxy_handler = ProxyHandler(dictProxies)
                opener = build_opener(proxy_handler).open
            else:
                opener = urlopen

            logger.info("wget %s/%s" % (cls.url_base, imagename))
            data = opener("%s/%s" % (cls.url_base, imagename),
                          data=None, timeout=cls.timeout).read()
            logger.info("Image %s successfully downloaded." % baseimage)

            try:
                with open(fullimagename, "wb") as outfile:
                    outfile.write(data)
            except IOError:
                raise IOError("unable to write downloaded \
                    data to disk at %s" % cls.image_home)

            if not os.path.isfile(fullimagename):
                raise RuntimeError("Could not automatically \
                download test images %s!\n \ If you are behind a firewall, \
                please set the environment variable http_proxy.\n \
                Otherwise please try to download the images manually from \n \
                %s" % (cls.url_base, imagename))
        else:
            data = open(fullimagename, "rb").read()
        fullimagename_bz2 = os.path.splitext(fullimagename)[0] + ".bz2"
        fullimagename_gz = os.path.splitext(fullimagename)[0] + ".gz"
        fullimagename_raw = os.path.splitext(fullimagename)[0]
        if not os.path.isfile(fullimagename_raw) or\
           not os.path.isfile(fullimagename_gz) or\
           not os.path.isfile(fullimagename_bz2):
            if imagename.endswith(".bz2"):
                decompressed = bz2.decompress(data)
                basename = fullimagename[:-4]
            elif imagename.endswith(".gz"):
                decompressed = gzip.open(fullimagename).read()
                basename = fullimagename[:-3]
            else:
                decompressed = data
                basename = fullimagename

            gzipname = basename + ".gz"
            bzip2name = basename + ".bz2"

            if basename != fullimagename:
                try:
                    open(basename, "wb").write(decompressed)
                except IOError:
                    raise IOError("unable to write decompressed \
                    data to disk at %s" % cls.image_home)
            if gzipname != fullimagename:
                try:
                    gzip.open(gzipname, "wb").write(decompressed)
                except IOError:
                    raise IOError("unable to write gzipped \
                    data to disk at %s" % cls.image_home)
            if bzip2name != fullimagename:
                try:
                    bz2.BZ2File(bzip2name, "wb").write(decompressed)
                except IOError:
                    raise IOError("unable to write bzipped2 \
                    data to disk at %s" % cls.image_home)
        return fullimagename

    @classmethod
    def download_images(cls, imgs=None):
        """
        Download all images needed for the test/benchmarks

        @param imgs: list of files to download
        """
        if not imgs:
            imgs = cls.ALL_DOWNLOADED_FILES
        for fn in imgs:
            print("Downloading from internet: %s" % fn)
            if fn[-4:] != ".bz2":
                if fn[-3:] == ".gz":
                    fn = fn[:-2] + "bz2"
                else:
                    fn = fn + ".bz2"
                print("  actually " + fn)
            cls.getimage(fn)

    @classmethod
    def get_options(cls):
        """
        Parse the command line to analyze options ... returns options
        """
        if cls.options is None:
            try:
                from argparse import ArgumentParser
            except:
                from fabio.third_party.argparse import ArgumentParser

            parser = ArgumentParser(usage="Tests for %s" % cls.name)
            parser.add_argument("-d", "--debug", dest="debug", help="run in debugging mode",
                                default=False, action="store_true")
            parser.add_argument("-i", "--info", dest="info", help="run in more verbose mode ",
                                default=False, action="store_true")
            parser.add_argument("-f", "--force", dest="force", help="force the build of the library",
                                default=False, action="store_true")
            parser.add_argument("-r", "--really-force", dest="remove",
                                help="remove existing build and force the build of the library",
                                default=False, action="store_true")
            parser.add_argument(dest="args", type=str, nargs='*')
            if IN_SOURCES:
                cls.options = parser.parse_args()
            else:
                cls.options = parser.parse_args([])
        return cls.options

    @classmethod
    def get_logger(cls, filename=__file__):
        """
        small helper function that initialized the logger and returns it
        """
        options = cls.get_options()
        dirname, basename = os.path.split(os.path.abspath(filename))
        basename = os.path.splitext(basename)[0]
        force_build = False
        force_remove = False
        level = logging.root.level
        if options.debug:
            level = logging.DEBUG
        elif options.info:
            level = logging.INFO
        if options.force:
            force_build = True
        if options.remove:
            force_remove = True
            force_build = True
        mylogger = logging.getLogger(basename)
        logger.setLevel(level)
        mylogger.setLevel(level)
        logging.root.setLevel(level)
        mylogger.debug("tests loaded from file: %s" % basename)
        if force_build:
            UtilsTest.forceBuild(force_remove)
        return mylogger


def recursive_delete(dirname):
    """
    Delete everything reachable from the directory named in "top",
    assuming there are no symbolic links.
    CAUTION:  This is dangerous!  For example, if top == '/', it
    could delete all your disk files.

    @param dirname: top directory to delete
    @type dirname: string
    """
    if not os.path.isdir(dirname):
        return
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(dirname)
