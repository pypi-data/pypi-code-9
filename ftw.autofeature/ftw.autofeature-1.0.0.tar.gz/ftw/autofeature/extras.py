from ftw.autofeature.utils import all_packages_installed
from ftw.autofeature.utils import combine_features
from ftw.autofeature.utils import find_extras_by_package
from ftw.autofeature.utils import find_package_by_module
from zope.interface import Interface
import logging


LOG = logging.getLogger('ftw.autofeature.extras')


class IDeclareExtrasFeaturesDirective(Interface):
    """Interface for the <autofeature:extras /> directive,
    which automatically declares directives for each extras in the
    current package.
    """


def declare_extras_features(context):
    LOG.debug('declaring extras for {0}'.format(context.info))
    package_name = find_package_by_module(context.package)
    extras = find_extras_by_package(package_name)
    LOG.debug('extras for {}: {}'.format(package_name, extras))

    installed_extras = [name for (name, dependencies) in extras.items()
                        if all_packages_installed(dependencies)]

    for postfix in combine_features(installed_extras):
        feature_name = '{}:{}'.format(package_name, postfix)
        LOG.debug('declaring feature {}'.format(feature_name))
        context.provideFeature(feature_name)
