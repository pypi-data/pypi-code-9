""" goulash.projects
"""
from __future__ import print_function
import os
from fabric import api
from fabric.colors import red, cyan
from fabric.contrib.console import confirm
from goulash._inspect import _main_package
from goulash._fabric import require_bin
VERSION_DELTA = .01


def project_search(fname, start=None):
    """ project-based directory tree search, where if the taget file
    isn't found in the working directory then you proceed upward until
    the file is found or you hit the file-system root. useful for
    project-style rc configuration data, say .git or .ackrc, etc.
    """
    start = start or os.getcwd()
    start = os.path.abspath(start)
    now = start
    while True:
        if fname in os.listdir(now):
            return os.path.join(now, fname)
        if os.path.dirname(now) == now:
            return None  # reached the root
        now = os.path.dirname(now)


def pypi_publish(pkg_root=None, src_root='.'):
    """ """
    user = os.environ.get('USER')
    home = os.environ.get('HOME')
    pypirc = os.path.join(home, '.pypirc')
    if not os.path.exists(pypirc):
        err = "FATAL: {0} does not exist, will not be able to publish to PyPi"
        err = err.format(home)
        raise SystemExit(err)
    pkg_root = pkg_root or _main_package(src_root)
    version_info = get_version_info(pkg_root)
    msg = [
        cyan("refreshing pypi for {0}=={1}".format(
            pkg_root, version_info)),
        red("you should have already bumped the "
            "versions and commited to (local) master!")]
    print('\n'.join(msg))
    assert user and home  # sometimes tox doesnt pass this
    err = 'To continue, try "pip install {0}" and try again'
    err = err.format('git+https://github.com/pypa/twine.git')
    require_bin('twine', err)
    try:
        ans = confirm(red('proceed with pypi update?'))
    except KeyboardInterrupt:
        print('aborting.')
        return
    if not ans:
        print('aborting.')
        return
    _pypi_publish(pkg_root, version_info)


def _pypi_publish(pkg_root, version_info):
    """ """
    api.local('git checkout -b pypi || git checkout pypi')
    api.local('git reset --hard master')
    api.local('python setup.py sdist')
    api.local('python setup.py register -r pypi')
    fname = os.path.join(
        'dist', '{0}-{1}.tar.gz'.format(
            pkg_root, version_info))
    assert os.path.exists(fname), 'no such file: ' + fname
    api.local("twine upload -r pypi --config-file ~/.pypirc {0}".format(fname))
    # python setup.py sdist upload -r pypi
    api.local("git push -f")
    print("leaving you in updated pypi branch")

def get_version_file(pkg_root):
    return os.path.join(pkg_root, 'version.py')

def get_version_info(pkg_root):
    sandbox = {}
    version_file = get_version_file(pkg_root)
    err = 'Version file not found in expected location: ' + version_file
    if not os.path.exists(version_file):
        raise SystemExit(err)
    execfile(version_file, sandbox)
    version_info = sandbox.get(
        'version',
        sandbox.get('__version__'))
    err = 'version info not found in version file: {0}'
    assert version_info is not None, err.format(vfile)
    return version_info


def version_bump(pkg_root=None, src_root='.'):
    """ bump the version number.

        to work, this function requires your version file to work like so:

            1. pkg/version.py exists
            2. pkg/version.py contains a '__version__' variable
            3. __version__ should be a number, not a string
            4. __version__ should be defined on the last line of the file
    """
    pkg_root = pkg_root or _main_package(src_root)
    print(red('bumping version number for package "{0}"'.format(
        pkg_root)))
    sandbox = {}
    current_version = get_version_info(pkg_root)  # sandbox['__version__']
    new_version = current_version + VERSION_DELTA
    version_file = get_version_file(pkg_root)
    with open(version_file, 'r') as fhandle:
        version_file_contents = [x for x in fhandle.readlines() if x.strip()]
    new_file = version_file_contents[:-1] + \
        ["__version__ = version = {0}\n".format(new_version)]
    new_file = '\n'.join(new_file)
    msg = "the current version will be changed to "
    msg = red(msg) + cyan("{0}\n".format(new_version))
    msg += red("new version file will look like this:\n\n")
    msg += cyan(new_file) + '\n'
    print(msg)
    try:
        ans = confirm(red('proceed with version change?'))
    except KeyboardInterrupt:
        print('aborting.')
        return
    else:
        if not ans:
            print('aborting.')
            return
        with open(version_file, 'w') as fhandle:
            fhandle.write(new_file)
            print('version has been rewritten.')
