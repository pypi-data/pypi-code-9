#!/usr/bin/env python
# #
# Copyright 2015-2015 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
# #
"""
Support for including additional Python modules, for easyblocks, module naming schemes and toolchains.

@author: Kenneth Hoste (Ghent University)
"""
import os
import sys
from vsc.utils import fancylogger

from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import expand_glob_paths, symlink
# these are imported just to we can reload them later
import easybuild.tools.module_naming_scheme
import easybuild.toolchains
import easybuild.toolchains.compiler
import easybuild.toolchains.fft
import easybuild.toolchains.linalg
import easybuild.toolchains.mpi
# importing easyblocks namespace may fail if easybuild-easyblocks is not available
# for now, we don't really care
try:
    import easybuild.easyblocks
    import easybuild.easyblocks.generic
except ImportError:
    pass


_log = fancylogger.getLogger('tools.include', fname=False)


# body for __init__.py file in package directory, which takes care of making sure the package can be distributed
# across multiple directories
PKG_INIT_BODY = """
from pkgutil import extend_path

# extend path so Python knows this is not the only place to look for modules in this package
__path__ = extend_path(__path__, __name__)
"""

# more extensive __init__.py specific to easybuild.easyblocks package;
# this is required because of the way in which the easyblock Python modules are organised in the easybuild-easyblocks
# repository, i.e. in first-letter subdirectories
EASYBLOCKS_PKG_INIT_BODY = """
from pkgutil import extend_path

# extend path so Python finds our easyblocks in the subdirectories where they are located
subdirs = [chr(l) for l in range(ord('a'), ord('z') + 1)] + ['0']
for subdir in subdirs:
    __path__ = extend_path(__path__, '%s.%s' % (__name__, subdir))

# extend path so Python knows this is not the only place to look for modules in this package
__path__ = extend_path(__path__, __name__)

del subdir, subdirs, l
"""


def create_pkg(path, pkg_init_body=None):
    """Write package __init__.py file at specified path."""
    init_path = os.path.join(path, '__init__.py')
    try:
        # note: can't use mkdir, since that required build options to be initialised
        if not os.path.exists(path):
            os.makedirs(path)

        # put __init__.py files in place, with required pkgutil.extend_path statement
        # note: can't use write_file, since that required build options to be initialised
        with open(init_path, 'w') as handle:
            if pkg_init_body is None:
                handle.write(PKG_INIT_BODY)
            else:
                handle.write(pkg_init_body)

    except (IOError, OSError) as err:
        raise EasyBuildError("Failed to create package at %s: %s", path, err)


def set_up_eb_package(parent_path, eb_pkg_name, subpkgs=None, pkg_init_body=None):
    """
    Set up new easybuild subnamespace in specified path.

    @param parent_path: directory to create package in, using 'easybuild' namespace
    @param eb_pkg_name: full package name, must start with 'easybuild'
    @param subpkgs: list of subpackages to create
    @parak pkg_init_body: body of package's __init__.py file (does not apply to subpackages)
    """
    if not eb_pkg_name.startswith('easybuild'):
        raise EasyBuildError("Specified EasyBuild package name does not start with 'easybuild': %s", eb_pkg_name)

    pkgpath = os.path.join(parent_path, eb_pkg_name.replace('.', os.path.sep))

    # handle subpackages first
    if subpkgs:
        for subpkg in subpkgs:
            create_pkg(os.path.join(pkgpath, subpkg))

    # creata package dirs on each level
    while pkgpath != parent_path:
        create_pkg(pkgpath, pkg_init_body=pkg_init_body)
        pkgpath = os.path.dirname(pkgpath)


def verify_imports(pymods, pypkg, from_path):
    """Verify that import of specified modules from specified package and expected location works."""
    for pymod in pymods:
        pymod_spec = '%s.%s' % (pypkg, pymod)
        try:
            pymod = __import__(pymod_spec, fromlist=[pypkg])
        # different types of exceptions may be thrown, not only ImportErrors
        # e.g. when module being imported contains syntax errors or undefined variables
        except Exception as err:
            raise EasyBuildError("Failed to import easyblock %s from %s: %s", pymod_spec, from_path, err)

        if not os.path.samefile(os.path.dirname(pymod.__file__), from_path):
            raise EasyBuildError("Module %s not imported from expected location (%s): %s",
                                 pymod_spec, from_path, pymod.__file__)

        _log.debug("Import of %s from %s verified", pymod_spec, from_path)


def include_easyblocks(tmpdir, paths):
    """Include generic and software-specific easyblocks found in specified locations."""
    easyblocks_path = os.path.join(tmpdir, 'included-easyblocks')

    set_up_eb_package(easyblocks_path, 'easybuild.easyblocks',
                      subpkgs=['generic'], pkg_init_body=EASYBLOCKS_PKG_INIT_BODY)

    easyblocks_dir = os.path.join(easyblocks_path, 'easybuild', 'easyblocks')

    allpaths = expand_glob_paths(paths)
    for easyblock_module in allpaths:
        filename = os.path.basename(easyblock_module)

        # generic easyblocks are expected to be in a directory named 'generic'
        parent_dir = os.path.basename(os.path.dirname(easyblock_module))
        if parent_dir == 'generic':
            target_path = os.path.join(easyblocks_dir, 'generic', filename)
        else:
            target_path = os.path.join(easyblocks_dir, filename)

        symlink(easyblock_module, target_path)

    included_ebs = [x for x in os.listdir(easyblocks_dir) if x not in ['__init__.py', 'generic']]
    included_generic_ebs = [x for x in os.listdir(os.path.join(easyblocks_dir, 'generic')) if x != '__init__.py']
    _log.debug("Included generic easyblocks: %s", included_generic_ebs)
    _log.debug("Included software-specific easyblocks: %s", included_ebs)

    # inject path into Python search path, and reload modules to get it 'registered' in sys.modules
    sys.path.insert(0, easyblocks_path)
    reload(easybuild)
    if 'easybuild.easyblocks' in sys.modules:
        reload(easybuild.easyblocks)
        reload(easybuild.easyblocks.generic)

    # sanity check: verify that included easyblocks can be imported (from expected location)
    for subdir, ebs in [('', included_ebs), ('generic', included_generic_ebs)]:
        pkg = '.'.join(['easybuild', 'easyblocks', subdir]).strip('.')
        loc = os.path.join(easyblocks_dir, subdir)
        verify_imports([os.path.splitext(eb)[0] for eb in ebs], pkg, loc)

    return easyblocks_path


def include_module_naming_schemes(tmpdir, paths):
    """Include module naming schemes at specified locations."""
    mns_path = os.path.join(tmpdir, 'included-module-naming-schemes')

    set_up_eb_package(mns_path, 'easybuild.tools.module_naming_scheme')

    mns_dir = os.path.join(mns_path, 'easybuild', 'tools', 'module_naming_scheme')

    allpaths = expand_glob_paths(paths)
    for mns_module in allpaths:
        filename = os.path.basename(mns_module)
        target_path = os.path.join(mns_dir, filename)
        symlink(mns_module, target_path)

    included_mns = [x for x in os.listdir(mns_dir) if x not in ['__init__.py']]
    _log.debug("Included module naming schemes: %s", included_mns)

    # inject path into Python search path, and reload modules to get it 'registered' in sys.modules
    sys.path.insert(0, mns_path)
    reload(easybuild.tools.module_naming_scheme)

    # sanity check: verify that included module naming schemes can be imported (from expected location)
    verify_imports([os.path.splitext(mns)[0] for mns in included_mns], 'easybuild.tools.module_naming_scheme', mns_dir)

    return mns_path


def include_toolchains(tmpdir, paths):
    """Include toolchains and toolchain components at specified locations."""
    toolchains_path = os.path.join(tmpdir, 'included-toolchains')
    toolchain_subpkgs = ['compiler', 'fft', 'linalg', 'mpi']

    set_up_eb_package(toolchains_path, 'easybuild.toolchains', subpkgs=toolchain_subpkgs)

    tcs_dir = os.path.join(toolchains_path, 'easybuild', 'toolchains')

    allpaths = expand_glob_paths(paths)
    for toolchain_module in allpaths:
        filename = os.path.basename(toolchain_module)

        parent_dir = os.path.basename(os.path.dirname(toolchain_module))

        # toolchain components are expected to be in a directory named according to the type of component
        if parent_dir in toolchain_subpkgs:
            target_path = os.path.join(tcs_dir, parent_dir, filename)
        else:
            target_path = os.path.join(tcs_dir, filename)

        symlink(toolchain_module, target_path)

    included_toolchains = [x for x in os.listdir(tcs_dir) if x not in ['__init__.py'] + toolchain_subpkgs]
    _log.debug("Included toolchains: %s", included_toolchains)

    included_subpkg_modules = {}
    for subpkg in toolchain_subpkgs:
        included_subpkg_modules[subpkg] = [x for x in os.listdir(os.path.join(tcs_dir, subpkg)) if x != '__init__.py']
        _log.debug("Included toolchain %s components: %s", subpkg, included_subpkg_modules[subpkg])

    # inject path into Python search path, and reload modules to get it 'registered' in sys.modules
    sys.path.insert(0, toolchains_path)
    reload(easybuild.toolchains)
    for subpkg in toolchain_subpkgs:
        reload(sys.modules['easybuild.toolchains.%s' % subpkg])

    # sanity check: verify that included toolchain modules can be imported (from expected location)
    verify_imports([os.path.splitext(mns)[0] for mns in included_toolchains], 'easybuild.toolchains', tcs_dir)
    for subpkg in toolchain_subpkgs:
        pkg = '.'.join(['easybuild', 'toolchains', subpkg])
        loc = os.path.join(tcs_dir, subpkg)
        verify_imports([os.path.splitext(tcmod)[0] for tcmod in included_subpkg_modules[subpkg]], pkg, loc)

    return toolchains_path
