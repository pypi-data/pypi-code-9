# coding: utf-8

import os
import livesettings
from setuptools import setup, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
CHANGES = open(os.path.join(os.path.dirname(__file__), 'CHANGES.md')).read()


setup(
    name='dj-livesettings',
    version=livesettings.__version__,
    packages=['livesettings'],
    include_package_data=True,
    license='MIT License',
    description='Django app that provides possibility to add settings that can be changed in DB.',
    long_description='\n\n'.join([README, CHANGES]),
    url='https://github.com/oeegor/dj-livesettings',
    author='Egor Orlov',
    author_email='oeegor@gmail.com',
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    cmdclass={
        'clean': CleanCommand,
    },
    install_requires=[
        'django-memoize>=1.2.0',
        'Django>=1.7',
    ],
)
