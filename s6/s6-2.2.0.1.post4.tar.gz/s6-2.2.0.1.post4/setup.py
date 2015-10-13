#!/usr/bin/env python
# this really only works on linux systems, at the moment
from __future__ import print_function

from os import environ
from os import system

# set $DISTUTILS_DEBUG to get extra output from distutils
environ['DISTUTILS_DEBUG'] = 'true'

from setuptools import setup
from distutils.core import Command
from setuptools.command.sdist import sdist as orig_sdist
from distutils.command.build import build as orig_build
from setuptools.command.install import install as orig_install


# ############# NOTES #####################
# setuptools.command.sdist.sdist

# setuptools/command/egg_info.py:egg_info.find_sources()
#   seems to be in charge of generating a file list
#   writes SOURCES.txt for its list
#   also reads MANIFEST.in; maybe this is the interface

# setuptools/command/sdist.py:add_defaults
#   adds various files to the file list based on the distribution object

# distutils/command/sdist.py:sdist.make_release_tree(base_dir, files)
#   copy files to base_dir. this will become the sdist


class build(orig_build):
    sub_commands = orig_build.sub_commands + [
        ('build_s6', None),
    ]


class install(orig_install):
    sub_commands = orig_install.sub_commands + [
        ('install_cexe', None),
    ]


class sdist(orig_sdist):
    def run(self):
        self.run_command('fetch_sources')
        return orig_sdist.run(self)


class fetch_sources(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        system('./get_sources.sh')


class build_s6(Command):
    def initialize_options(self):
        self.build_temp = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'))

    def run(self):
        self.run_command('fetch_sources')
        cmd = './build.sh %s' % self.build_temp
        print(cmd)
        system(cmd)


class install_cexe(Command):
    description = 'install C executables'
    outfiles = ()

    def initialize_options(self):
        self.build_dir = self.install_dir = None

    def finalize_options(self):
        # this initializes attributes based on other commands' attributes
        self.set_undefined_options('build', ('build_temp', 'build_dir'))
        self.set_undefined_options(
            'install', ('install_data', 'install_dir'))

    def run(self):
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)

    def get_outputs(self):
        return self.outfiles


cmdclass = {
    'sdist': sdist,
    'fetch_sources': fetch_sources,
    'build': build,
    'build_s6': build_s6,
    'install': install,
    'install_cexe': install_cexe,
}


def wheel_support():
    class bdist_wheel(orig_bdist_wheel):
        def get_tag(self):
            python, abi, plat = orig_bdist_wheel.get_tag(self)
            python = 'py2.py3'  # python is irrelevant to our pure-C package
            return python, abi, plat

    cmdclass['bdist_wheel'] = bdist_wheel

try:
    from wheel.bdist_wheel import bdist_wheel as orig_bdist_wheel
except ImportError:
    pass
else:
    wheel_support()


setup(
    name='s6',
    version='2.2.0.1-4',
    cmdclass=cmdclass,
)
