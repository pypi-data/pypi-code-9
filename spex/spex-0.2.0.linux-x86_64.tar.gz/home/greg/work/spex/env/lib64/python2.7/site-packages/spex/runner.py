from __future__ import print_function
import os
import sys
import logging
logger = logging.getLogger('spex')  # noqa

from .artifact_server import ArtifactServer
from .utils import establish_spark_home, honor_logging

def driver(application, application_args, spex_conf, verbose=False):
    """Runs the spex in driver mode, creating the actual application from its entry point with PySpark configuration

    Parameters
    ----------
    args : dict-like
        The arguments presented to the spex application, used for configuring PySpark and booting the driver.
    prog : str
        The name of the spex application that is running the PySpark jobs
    """
    honor_logging(verbose)
    spex_conf = establish_spark_home(spex_conf)
    sys.path.append(spex_conf.spex_root)

    # You must import this *after* you have got spark onto the sys.path
    from .context import SpexContext

    with ArtifactServer(os.getcwd()) as artifact_server:
        artifact_resolver = artifact_server.artifact_uri_resolver()
        logger.info('Started artifact server [%s]', artifact_server)

        with SpexContext(spex_conf, artifact_resolver) as spex_context:
            logger.debug('Application in use is [%s]', application)
            application.configure_spark_context(application_args, spex_context.spark_config)

            logger.info('Starting spark application from spex file')
            application.run(spex_context)


def daemon():
    """Runs the spex in daemon mode, booting the environment ready for PySpark to manipulate it for operation"""
    try:
        import pyspark.daemon
        pyspark.daemon.manager()
    except ImportError:
        raise ImportError('PySpark not correctly setup?')
