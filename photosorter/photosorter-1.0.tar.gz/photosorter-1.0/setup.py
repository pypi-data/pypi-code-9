import os
from setuptools import setup

def _read(file):
    return open(file, 'rb').read()

setup(
    name='photosorter',
    version='1.0',
    packages=[],
    scripts=['photosorter'],
    install_requires=[
        'Pillow>=2.3.0',
        'six>=1.5.2',
    ],
    include_package_data=True,
    license='BSD License',
    description='Photo organizing app',
    long_description=_read('README.md').decode('utf-8'),
    url='https://github.com/iamtio/photosorter',
    author='Igor Tsarev',
    author_email='iam@tio.so',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
