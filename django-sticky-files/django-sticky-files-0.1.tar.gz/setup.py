import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# Some initialization
here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.rst')).read()


data_files = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)


# this code snippet is taken from django-registration setup.py script
for dirpath, dirnames, filenames in os.walk('sticky_files'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        prefix = dirpath[len('sticky_files')+1:]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name="django-sticky-files",
    version="0.1",
    packages=find_packages(),
    author="asyncee",
    description="Application to make Django file fields save their values between page reloads",
    long_description=long_description,
    license="MIT",
    keywords="django sticky_files",
    url='https://github.com/asyncee/django-sticky-files',
    download_url='https://pypi.python.org/pypi/django-sticky-files/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Widget Sets',
    ],

    package_dir={'sticky_files': 'sticky_files'},
    package_data={'sticky_files': data_files},
    zip_safe=False,

    tests_require=['tox'],
    cmdclass={'test': Tox},
)
