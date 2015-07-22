#!/usr/bin/env python

from setuptools import setup, os
from setuptools.command.install import install
from subprocess import call


class NpmInstall(install):
    def run(self):
        install.run(self)
        call(['npm', 'install'],
             cwd=os.path.join(self.install_lib, 'pybabel_htmlbars'))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pybabel-htmlbars',
    version='0.1.0',
    author='Eliksir AS',
    author_email='code@e5r.no',
    description='Pybabel HTMLBars gettext strings extractor',
    license='BSD',
    keywords='pybabel htmlbars gettext i18n',
    url='https://github.com/eliksir/pybabel-htmlbars',
    packages=['pybabel_htmlbars'],
    long_description=read('README.rst'),
    install_requires=[
        'pexpect-u'
    ],
    include_package_data=True,
    entry_points='''
        [babel.extractors]
        hbs = pybabel_htmlbars.extractor:extract_htmlbars
        ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Topic :: Software Development :: Internationalization',
    ],
    cmdclass={
        'install': NpmInstall,
    }
)
