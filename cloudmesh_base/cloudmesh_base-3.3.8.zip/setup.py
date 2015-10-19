#! /usr/bin/env python
from __future__ import print_function

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
from cloudmesh_base.util import banner
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.setup import os_execute,  check_pip

from cloudmesh_base import __version__

check_pip()

requirements = ['wheel',
                'tox',
                'nose',
                'future',
                'docopt',
                'prettytable',
                'pyaml',
                'pytimeparse==1.1.4',
                'pyyaml',
                'simplejson']


banner("Installing cloudmesh_base {:}".format(__version__))

home = os.path.expanduser("~")


class Make(object):

    @classmethod
    def github(cls):
        commands = """
            git commit -a
            git push
            """
        os_execute(commands)
    
    @classmethod
    def clean(cls):
        commands = """
            rm -rf docs/build
            rm -rf build
            rm -rf cloudmesh_base.egg-info
            rm -rf dist
            """
        os_execute(commands)

    @classmethod        
    def doc(cls):
        cls.install()
        commands = """
            sphinx-apidoc -o docs/source cloudmesh_base
            cd docs; make -f Makefile html
            """
        os_execute(commands)    

    @classmethod
    def pypi(cls):
        cls.clean()
        cls.install()
        commands = """
            python setup.py install
            python setup.py bdist_wheel upload
            python setup.py sdist --format=bztar,zip upload
            """
        os_execute(commands)    

    @classmethod
    def pypitest(cls):
        cls.clean()
        cls.install()
        commands = """
            python setup.py bdist_wheel
            python setup.py sdist --format=bztar,zip upload -r https://testpypi.python.org/pypi
            """
        os_execute(commands)    
        
    @classmethod
    def install(cls):
        cls.clean()
        commands = """
            python setup.py install
            """
        os_execute(commands)    

    @classmethod
    def install_requirements(cls):
        for requirement in requirements:
            os.system("pip install {:}".format(requirement))

#
# INSTALL
#

class CleanPackage(install):
    def run(self):
        Make.clean()

            
class UploadToPypi(install):
    """Upload the package to pypi."""
    def run(self):
        Make.pypi()

class UploadToPypitest(install):
    """Upload the package to pypi."""
    def run(self):
        Make.pypitest()

        
class RegisterWithPypi(install):
    """Upload the package to pypi."""
    def run(self):
        banner("Register with Pypi")
        # os.system("python shell_plugins.py register")
        print ("not implemented")
        
class InstallBase(install):
    """Install the package."""
    def run(self):
        banner("Requirements")
        Make.install_requirements()
        banner("Install Cloudmesh Base")
        # os.system("pip install pip -U")
        install.run(self)


class InstallRequirements(install):
    """Install the requirements."""
    def run(self):
        auto_create_requirements()
        banner("Install Cloudmesh Base Requirements")
        os.system("pip install -r requirements.txt")
        

class InstallAll(install):
    """Install requirements and the package."""
    def run(self):
        banner("Install Cloudmesh Base Requirements")
        os.system("pip install -r requirements.txt")
        banner("Install Cloudmesh Base")        
        install.run(self)


class CreateDoc(install):
    """Install requirements and the package."""

    def run(self):
        Make.doc()

class PushPackage(install):
    """Install requirements and the package."""

    def run(self):
        Make.github()

setup(
    name='cloudmesh_base',
    version=__version__,
    description='A set of simple base functions and classes useful for cloudmesh and other programs',
    # description-file =
    #    README.rst
    author='The Cloudmesh Team',
    author_email='laszewski@gmail.com',
    url='http://github.org/cloudmesh/base',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Boot',
        'Topic :: System :: Systems Administration',
        'Framework :: Flask',
        'Environment :: OpenStack',
    ],
    entry_points={
        'console_scripts': [
            'cm-authors = cloudmesh_base.gitinfo:GitInfo.print_authors',
        ],
    },
    install_requires=requirements,
    packages=find_packages(),
    cmdclass={
        'install': InstallBase,
        'requirements': InstallRequirements,
        'all': InstallAll,
        'pypi': UploadToPypi,
        'pypitest': UploadToPypitest,        
        'pypiregister': RegisterWithPypi, 
        'doc': CreateDoc,
        'clean': CleanPackage,
        'push': PushPackage,
        },
)

