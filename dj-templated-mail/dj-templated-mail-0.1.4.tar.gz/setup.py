# coding: utf-8

import os
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
    name='dj-templated-mail',
    version='0.1.4',
    packages=['dj_templated_mail'],
    include_package_data=True,
    license='MIT License',
    description='Django app that provides possibility to render email messages from templates stored in DB.',
    long_description='\n\n'.join([README, CHANGES]),
    url='https://github.com/oeegor/dj-templated-mail#django-templated-mail/',
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
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    cmdclass={
        'clean': CleanCommand,
    }
)
