
VERSION = '0.6.0'

#pylint:disable=missing-docstring,unused-import,import-error

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

LONG_DESCRIPTION = open("README.txt").read()

setup(
    name="mercurial_extension_utils",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='http://bitbucket.org/Mekk/mercurial-extension_utils',
    description='Mercurial Extension Utils',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=['mercurial_extension_utils'],
    keywords="mercurial hg extension",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control',
        # 'Topic :: Software Development :: Version Control :: Mercurial',
    ],
    zip_safe=True)
