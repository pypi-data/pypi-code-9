from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='cfnparams',
    version='0.4',
    description='CloudFormation stack paramater utility.',
    author='Jonathan Sokolowski',
    author_email='jsok@expert360.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws cfn cloudformation stack',
    url='https://github.com/expert360/cfn-params',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto>=2.38.0',
        'retrying>=1.3.3',
    ],
    entry_points={
        'console_scripts': [
            'cfn-params = cfnparams:main',
        ],
    },
    tests_require=['tox'],
    cmdclass = {'test': Tox},
)
