"""
the pytest-capturelog plugin breaks the slogging as it
sets up all loglevels to logging.NOTSET before every test

partitial solution other than uninstalling capturelog or --nocapure option
is to globally set
logging.NOTSET = logging.INFO
"""

from ethereum.slogging import get_logger, configure_logging
import logging
configure_logging('mytest:info')  # INFO we say!

logger = get_logger('mytest')


def test_unexpected_trace():
    logger.debug('this message is unexpected')
    assert False


def test_unexpected_trace_fixed():
    # logging.NOTSET = logging.INFO  # this can also be set at the beginning of the test file
    logger.trace('this message is unexpected')
    assert False
