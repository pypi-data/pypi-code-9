# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


setup(name='django-ipapi',
      version=__import__('ipapi').get_version(),
      description='Django IP-API.com wrapper',
      long_description=README,
      url='https://bitbucket.org/sizeof/django-ipapi',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django ip blocking api ip-api.com',
      author=u'Mariusz Smenżyk',
      author_email='mariusz.smenzyk@sizeof.pl',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      dependency_links=[],
      install_requires=[
          'setuptools',
          'django-ipware',
      ],
)
