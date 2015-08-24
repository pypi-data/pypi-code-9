from zope.interface import Interface
import logging


LOG = logging.getLogger('ftw.autofeature.extras')


class IDumpFeaturesDirective(Interface):
    """Interface for the <autofeature:dump /> directive,
    which dumps all currently registered features.
    """


def dump_features(context):
    print 'Currently registered ZCML features (by autofeature:dump):'
    for name in sorted(context._features):
        print '- ', name
