from setuptools import setup, find_packages

import os

HERE = os.path.dirname(__file__)

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

touch(os.path.join(HERE, 'src', 'django_tests', '__init__.py'))

setup(
    name='django-tests',
    version='1.8.3',
    url='https://github.com/moreati/django-tests',
    author='Django Software Foundation',
    author_email='foundation@djangoproject.com',
    maintainer='Alex Willmer',
    maintainer_email='alex@moreati.org.uk',
    description='The Django test suite, as an installable package.',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'':'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
