from distutils.core import setup

__author__ = 'jpercent'

packages = ['quanttus_api']
package_data = {
    'quanttus_api' : ['conf.json']
}

setup(
    name='quanttus_api',
    version='0.1.2',
    packages=packages,
    package_data=package_data,
    author='Quanttus',
    author_email='software@quanttus.com',
    scripts=['bin/quanttus-upload'],
    requires=['requests']
)
