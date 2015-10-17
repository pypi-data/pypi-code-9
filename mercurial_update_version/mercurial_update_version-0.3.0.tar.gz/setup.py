
VERSION = '0.3.0'

#pylint:disable=missing-docstring,unused-import,import-error

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

LONG_DESCRIPTION = open("README.txt").read()

setup(
    name="mercurial_update_version",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='http://bitbucket.org/Mekk/mercurial-update_version',
    description='Mercurial Update Version Extension',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=['update_version'],
    install_requires=[
        'mercurial_extension_utils>=0.8.1',
    ],
    keywords="mercurial hg version auto-update tag",
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: DFSG approved',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Version Control'
    ],
    zip_safe=True)
