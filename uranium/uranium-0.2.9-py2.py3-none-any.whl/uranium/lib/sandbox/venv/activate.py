import os
import sys
import pkg_resources

from pip._vendor import pkg_resources as pip_pkg_resources


def activate_virtualenv(root):
    """ this will activate a virtualenv in the case one exists """
    # sys.prefix = os.path.join(*sys.prefix.split(os.sep)[:-2])
    old_prefix = sys.prefix
    sys.path = [p for p in sys.path if sys.prefix not in p]

    activate_this_path = os.path.join(root, 'bin', 'activate_this.py')
    with open(activate_this_path) as fh:
        exec(fh.read(), {'__file__': activate_this_path}, {})

    sys.path += [
        os.path.join(root, 'lib', 'python%s' % sys.version[:3], 'lib-dynload')
    ]

    # we modify the executable directly
    # because pip invokes this to install packages.
    sys.executable = os.path.join(root, 'bin', 'python')

    for _pkg_resources in [pkg_resources, pip_pkg_resources]:
        _clean_package_resources(_pkg_resources, old_prefix)

    # in the past, an incorrect real_prefix directory was being
    # generated when using uranium. it looks like sys.prefix
    # works as a replacement, so let's use that.
    sys.real_prefix = sys.prefix


def _clean_package_resources(_pkg_resources, old_prefix):
    # this is a workaround for pip. Pip utilizes pkg_resources
    # and the path to determine what's installed in the current
    # sandbox
    #
    # we remove the requirements that are installed
    # from the parent environment, so pip will detect
    # the requirement from the current virtualenv
    for name, req in list(_pkg_resources.working_set.by_key.items()):
        if old_prefix in req.location:
            del _pkg_resources.working_set.by_key[name]

    # ensure that pkg_resources only searches the
    # existing sys.path. These variables are set on
    # initialization, so we have to reset them
    # when activating a sandbox.
    _pkg_resources.working_set.entries = sys.path
