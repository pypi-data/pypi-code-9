"""
BrowserPlus
-----------

Advanced Mechanize browser.

"""
from setuptools import setup, find_packages
from browserplus import __version__

setup(
    name='browserplus',
    version=__version__,
    url='https://github.com/vinceau/browserplus',
    license='MIT',
    author='Vince Au',
    author_email='vinceau09@gmail.com',
    description='Advanced Mechanize browser.',
    long_description=__doc__,
    data_files=[('browserplus', ['README.rst'])],
    packages=find_packages(),
    install_requires=['mechanize', 'lxml', 'cssselect'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

