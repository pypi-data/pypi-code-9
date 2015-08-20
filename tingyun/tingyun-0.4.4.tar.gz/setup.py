from __future__ import print_function

with_setuptools = False

try:
    from setuptools import setup
    with_setuptools = True
except ImportError:
    from distutils.core import setup

from distutils.core import Extension
from distutils.sysconfig import get_python_lib
from distutils.command.build_ext import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError, DistutilsPlatformError)

import os
import sys


# Dynamically calculate the version based on tingyun.VERSION.
version = __import__('tingyun').get_version()
_copyright = '(C) Copyright 2007-2015 networkbench Inc. All rights reserved.'

# detect it is reinstall or not. overwrite maybe cause some problem.
overlay_warning = False
existing_path = None
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "tingyun"))
        if os.path.exists(existing_path):
            overlay_warning = True
            break


def full_split(dir_path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(dir_path)
    if head == '':
        return [tail] + result
    if head == dir_path:
        return result
    return full_split(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have an easy way to do this.
packages, package_data = [], {}
root_dir = os.path.dirname(__file__)
tingyun_dir = 'tingyun'
if root_dir != '':
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(tingyun_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = full_split(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames:
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

kwargs = dict(
    name="tingyun",
    version=version,
    description="python agent",
    long_description="Python agent for Ting Yun",
    author="Networkbench",
    author_email="python@networkbench.com ",
    license=_copyright,
    platforms=['unix', 'linux'],
    url="http://www.tingyun.com",
    packages=packages,
    package_data={'tingyun': ['tingyun.ini', 'api/requests/cacert.pem']},
    scripts=['scripts/tingyun-admin'],
)

if with_setuptools:
    kwargs['entry_points'] = {'console_scripts': ['tingyun-admin = tingyun.admin:main']}

if sys.platform == 'win32' and sys.version_info > (2, 6):
    build_ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError)
else:
    build_ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)


class BuildExtFailed(Exception):
    pass


class OptionalBuildExt(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildExtFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except build_ext_errors:
            raise BuildExtFailed()


def _run_setup(with_extension):
    """
    :param with_extension:
    :return:
    """
    setup_kwargs = dict(kwargs)

    if with_extension:
        setup_kwargs['ext_modules'] = [
            Extension("tingyun.api.wrapt._wrappers", ["tingyun/api/wrapt/_wrappers.c"])
        ]

    setup_kwargs['cmdclass'] = dict(build_ext=OptionalBuildExt)
    setup(**setup_kwargs)


def do_run_setup_install():
    """
    :return:
    """
    with_extensions = True

    # skip the pypy.
    if hasattr(sys, 'pypy_version_info'):
        with_extensions = False
        print('========================================================')

    try:
        _run_setup(with_extensions)
    except Exception as _:
        print(80 * '*')

        print("""
                                  =========================================
                                               WARNING
                                  =========================================
                The optional C extension components of the Python agent could not be compiled.
              This can occur where a compiler is not present on the target system or the Python installation does not
              have the corresponding developer package installed. The Python agent will instead be installed without
              the extensions. The consequence of this is that although the Python agent will still run,
              JSON encoding/decoding speedups will not be available,
              nor will some of the non core features of the Python agent."""
        )

        print("INFO: Trying to build without extensions.")
        print(80 * '*')

        _run_setup(with_extension=False)
        print(80 * '*')
        print("INFO: Only pure Python agent was installed.")

        print(80 * '*')

# Actually run the setup for agent.
do_run_setup_install()

if overlay_warning and False:
    print("""
                            =========================================
                                            WARNING!
                            =========================================
   You have just installed agent over top of an existing installation, without removing it first.
 Because of this, your install may now include extraneous files from a previous version that have
 since been removed from tingyun. This maybe cause a variety of problems. You should manually
 remove the

 %(existing_path)s

 directory and re-install tingyun agent.

""" % {"existing_path": existing_path})
