# -*- extra stuff goes here -*-

from Globals import DevelopmentMode
import logging
import os

logger = logging.getLogger('rt.filenotindexed')


TRUISMS = ['yes', 'y', 'true', 'on']
DISABLED = os.environ.get('DISABLE_FILE_INDEXING', None)

def checkPatchingEnabled():
    return  (DISABLED is not None and DISABLED.lower() in TRUISMS) or \
            (DISABLED is None and DevelopmentMode is True)
    

if checkPatchingEnabled():
    # Yes! I copied this all from Products.PrintingMailHost
    logger.warning("Hold on to your hats folks, I'm patching")
    import monkeys


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
