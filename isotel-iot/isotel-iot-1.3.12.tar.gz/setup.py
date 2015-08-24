import os
import re
from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Enables ``setup.py clean`` command to clean up leftover directories properly.
    The default ``clean`` leaves a ``*.egg-info`` directory. This custom class takes care of that.
    """
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


def extract_version(verfile):
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"

    with open(verfile, "rt") as f:
        data = f.read()
        mo = re.search(VSRE, data, re.M)

    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (verfile,))


short_desc = ('An API interface to communicate with an ISOTEL of Things (IoT) server, '
              'used to manage hardware devices like sensors, actuators, etc.')

long_desc = ('IoT library is an API interface to communicate '
             'with an ISOTEL of Things (IoT) server.\n'
             'An IoT server provides innovative ways to interact with hardware devices '
             'like sensors, actuators connected via serial links, USB, bluetooth, wireless, etc., '
             'in a distributed, profile-less manner, to support heterogeneity and scalability.\n'
             'isotel-iot API can bind to an IoT server, search for available devices, '
             'as well as interact with them by retrieving and modifying their values.\n'
             'IoT servers can connect to each others via Skype, '
             'a feature extremely useful to reach out to remote devices behind firewalls.')

setup(
    name='isotel-iot',
    version=extract_version('isotel/IoT/_version.py'),
    url='http://www.isotel.eu/IoT',
    author='Tine Kavcic, Uros Platise, Jayesh Bhoot',
    author_email='pypi@isotel.eu',
    license='MIT',
    description=short_desc,
    long_description=long_desc,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='internet web things heterogeneous scalable sensors hardware devices DIY',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    cmdclass={
        'clean': CleanCommand
    }
)
