try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '2.0.1'

setup(
    name='VTUResults',
    version=version,
    install_requires=['requests>=2.6.0', 'BeautifulSoup4>=4.3.1'],
    author='Mahesh Kumar',
    author_email='maheshk2194@gmail.com',
    packages=['vr'],
    #test_suite='tests',
    url='https://github.com/maheshkkumar/VTUResults/',
    license='GNU General Public License (GPL)',
    description='Python Package for accessing VTU Results.',
    long_description='Python Package for accessing Visvesvaraya Technological University Results.'
                     ' Usage : https://github.com/maheshkkumar/VTUResults.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
