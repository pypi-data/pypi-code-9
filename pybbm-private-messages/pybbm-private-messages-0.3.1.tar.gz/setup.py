import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pybbm-private-messages',
    version='0.3.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pybbm',
        'django_select2'
    ],
    test_suite='runtests.runtests',
    license='MIT License',
    description='A private messaging plugin for the pybbm forum.',
    long_description=README,
    url='https://github.com/skolsuper/pybbm_private_messages',
    author='James Keys',
    author_email='skolsuper@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

