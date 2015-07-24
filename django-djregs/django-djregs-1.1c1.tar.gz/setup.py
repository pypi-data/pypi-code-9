from setuptools import setup, find_packages

from registration import get_version

setup(
    name='django-djregs',
    version=get_version().replace(' ', '-'),
    description='Handle user registration and email verification with Django',
    author='SF Software limited t/a Pebble',
    author_email='sysadmin@talktopebble.co.uk',
    url='https://github.com/mypebble/djregs',
    package_dir={'registration': 'registration'},
    packages=find_packages(),
    classifiers=['Development Status :: 5 - Production/Stable',
               'Environment :: Web Environment',
               'Framework :: Django',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: Utilities'],
)
