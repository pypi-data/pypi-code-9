# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import glob

import logging
import platform
import codecs
import tarfile

from . import __version__ as spex_version  # noqa
logger = logging.getLogger('spex')  # noqa


def uber_distro_location(spark_name, base_location=os.curdir):
    spark_distro = spark_name + '.tar.bz2'
    spark_distro_location = os.path.abspath(os.path.join(base_location, spark_distro))
    return spark_distro_location


def establish_spark_distro(spark_distro_location, spark_home, spark_name, spex_file, spex_name):
    """Given a spark distribution, and a spex distribution create a new tarball that
    includes everything needed to bring up the application from first start

    Parameters
    ----------
    spark_home : str
        The location of the spark distribution

    spark_name : str
        The name used for spark

    spex_file : str
        The location of the spex file

    spex_name : str
        The name given to the spex application
    """
    with tarfile.open(spark_distro_location, 'w:bz2') as tarball:
        tarball.add(spex_file, arcname=spex_name)
        tarball.add(spark_home, arcname=spark_name)
    logger.info('Created spark_distribution [%s]', spark_distro_location)


def establish_spark_home(spex_config):
    """Given a home, get everything setup in python to get spark onto the sys.path

    Parameters
    ----------
    spex_config : spex.config.SpexConfig
        The configuration for this spex application

    Returns
    -------
    spex_config : spex.config.SpexConfig
        The configuration presented, since it might have been modified by spex
    """
    assert spex_config.spark_distro is None, "Distribution mode is not _yet_ supported"
    home = spex_config.spark_config.spark_home

    assert home, "How did we get started without a spark_home"
    spark_home = os.path.realpath(os.path.abspath(home))
    spark_name = os.path.basename(spark_home)
    if 'SPARK_HOME' not in os.environ or os.environ['SPARK_HOME'] != spark_home:
        os.environ['SPARK_HOME'] = spark_home

    python_lib = os.path.join(os.path.abspath(spark_home), 'python')
    assert os.path.exists(python_lib), 'Python path does not exist in spark_home'
    py4j = glob.glob(os.path.join(python_lib, '**', 'py4j-*.zip'))
    assert len(py4j) == 1, 'Incorrect number of py4j deps'
    py4j_path = os.path.abspath(py4j[0])
    assert os.path.exists(py4j_path), 'How does this even happen !'
    sys.path.insert(0, python_lib)
    sys.path.insert(0, py4j_path)

    spex_name = spex_config.spex_name
    spex_file = spex_config.spex_file

    assert spex_name
    assert spex_file

    # No spark_distro ? We need to tar one up to service it
    spark_distro = uber_distro_location(spark_name)
    if not os.path.exists(spark_distro):
        logger.info('Could not find a local spark distribution tarball will make one from SPARK_HOME [%s]', spark_home)
        establish_spark_distro(spark_distro, spark_home, spark_name, spex_file, spex_name)
    else:
        logger.info('Using spark distribution found at [%s]', spark_distro)
    return spex_config._replace(spark_distro=spark_distro)


def honor_logging(level=logging.INFO):
    """Can be called to turn on log messages

    This is best done where you are sure that you are not running in the daemon mode, which *must* print the port
    that the surrogate spark process is running on as the very first thing on stdout

    Parameters
    ----------
    level : logging.level, optional
        The logging level to change to, defaults to INFO
    """
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(level)


def print_banner(spex_context):
    """Print a friendly, welcome to spex banner

    Parameters
    ----------
    spex_context : spex.context.SpexContext
        The context object that carries details about spex and spark

    """
    python_ver = ' '.join((platform.python_implementation(), platform.python_version()))
    spark_ver = spex_context.sc.version

    # pylint:disable=anomalous-backslash-in-string
    print(u'''
    ███████╗██████╗ ███████╗██╗  ██╗
    ██╔════╝██╔══██╗██╔════╝╚██╗██╔╝
    ███████╗██████╔╝█████╗   ╚███╔╝
    ╚════██║██╔═══╝ ██╔══╝   ██╔██╗
    ███████║██║     ███████╗██╔╝ ██╗
    ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝ version %s

    ============ Welcomes you to ==============
       ____              __
      / __/__  ___ _____/ /__
     _\ \/ _ \/ _ `/ __/  '_/
    /__ / .__/\_,_/_/ /_/\_\   version %s
       /_/

    You are flying with:
        Python: %s

    ''' % (spex_version, spark_ver, python_ver), file=codecs.getwriter('utf8')(sys.stderr))


class ArtifactResolver(object):
    """Class that encapsulates the behaviour of resolving filenames to an artifact server"""

    def __init__(self, uri_template):
        """Create a new resolver that uses the given uri_template to construct uris

        Parameters
        ----------
        uri_template : str
            A python interpolation string that can be used to construct uris
        """
        self.uri_template = uri_template

    def __call__(self, name):
        """Resolve artifact names to uris

        Parameters
        ----------
        name : str
            The name / file to get a URI for

        Returns
        -------
        artifact_uri : str
            The artifact uri for the given file name
        """
        return self.uri_template % name

    def to_dict(self):
        """Dump the class out to a dict for serialisation"""
        return {'uri_template': self.uri_template}

    @classmethod
    def from_dict(cls, raw_dict):
        return ArtifactResolver(raw_dict['uri_template'])
