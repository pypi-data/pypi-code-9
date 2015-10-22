from setuptools import setup, find_packages
from setuptools.command.test import test


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests
        runtests()


setup(
    name='django-dadaviews',
    version='0.0.3',
    description='A very simple class based views implementation for Django.',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    license='ISC',
    url='https://github.com/aino/django-dadaviews',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    cmdclass={"test": TestCommand},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
)
