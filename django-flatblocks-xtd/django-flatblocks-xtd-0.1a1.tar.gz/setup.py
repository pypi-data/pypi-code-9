import os
import sys

try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools.command.test import test


def run_tests(*args):
    srcdir = os.path.abspath(os.path.curdir)
    sys.path.insert(0, os.path.join(srcdir, 'test_project'))
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

    from django.conf import settings
    from django.test.utils import get_runner

    runner = get_runner(settings, "django.test.simple.DjangoTestSuiteRunner")
    test_suite = runner(verbosity=2, interactive=True, failfast=False)
    errors = test_suite.run_tests(['flatblocks_xtd'])
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)
    
test.run_tests = run_tests

setup(
    name = 'django-flatblocks-xtd',
    version = '0.1a1',
    description = 'django-flatblocks-xtd acts like django-flatblocks but '
                  'adds support for markup content with django-markup and '
                  'inline media content with django-inline-media.',
    long_description = open('README.rst').read(),
    keywords = 'django apps',
    license = 'New BSD License',
    author = 'Daniel Rus Morales',
    author_email = 'mbox@danir.us',
    url = 'http://github.com/danirus/django-flatblocks-xtd/',
    dependency_links = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(exclude=['ez_setup', 'test_project']),
    include_package_data = True,
    zip_safe = False,
    test_suite = "dummy",
)
