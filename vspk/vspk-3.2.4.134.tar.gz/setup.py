from setuptools import setup
import os

packages = ['vspk', 'vspk.vsdk']
vsdks_path = "./vspk/vsdk"
package_data = {}

for item in os.listdir(vsdks_path):
    if os.path.isfile("%s/%s" % (vsdks_path, item)):
        continue

    packages.append("vspk.vsdk.%s" % item)
    packages.append("vspk.vsdk.%s.fetchers" % item)
    packages.append("vspk.vsdk.%s.autogenerates" % item)

    package_data["vspk.vsdk.%s" % item] = ['resources/*']

setup(
    name='vspk',
    version='3.2.4.134',
    author='Antoine Mercadal, Christophe Serafin',
    author_email='antoine@nuagenetworks.net, christophe.serafin@nuagenetworks.net',
    packages=packages,
    package_data=package_data,
    description='Nuage Networks VSP Software Development Kit',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
    license='BSD-3',
    url='https://github.com/nuagenetworks',
    # include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ]
)
