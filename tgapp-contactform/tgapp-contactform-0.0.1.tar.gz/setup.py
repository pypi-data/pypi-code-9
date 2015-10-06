# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.3.5",
    "tgext.pluggable",
    "tgext.mailer"
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-contactform',
    version='0.0.1',
    description='tgapp-contactform is a Pluggable application for TurboGears2 that shows a simple contact form.',
    long_description=README,
    author='AXANT',
    author_email='tech@axant.it',
    url='https://bitbucket.org/axant/tgapp-contactform',
    keywords='turbogears2.application',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'contactform': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'contactform': [
            ('**.py', 'python', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)
    ]},
    entry_points="""
    """,
    zip_safe=False
)
