# -*- coding: UTF-8 -*-

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import sys
import os

version = sys.version_info[0]
if version > 2:
    pass
else:
    pass


class CustomInstallCommand(install):
    def run(self):
        install.run(self)


def find_data(packages, extensions):
    data = {}
    for package in packages:
        package_path = package.replace('.', '/')
        for dirpath, _, filenames in os.walk(package_path):
            for filename in filenames:
                for extension in extensions:
                    if filename.endswith(".%s" % extension):
                        file_path = os.path.join(
                            dirpath,
                            filename
                        )
                        file_path = file_path[len(package) + 1:]
                        if package not in data:
                            data[package] = []
                        data[package].append(file_path)
    return data

setup(
    name = "syrpc",
    version = "1.0",
    packages = find_packages(),
    package_data=find_data(
        find_packages(), ["json", "json.gz"]
    ),
    entry_points = {
        'console_scripts': [
            'syrpc-test-client        = syrpc.runner:run_client',
            'syrpc-test-server        = syrpc.runner:run_server',
            'syrpc-test-server-forever = syrpc.runner:run_server_forever',
        ]
    },
    install_requires = [
        'siphashc3',
        'kombu',
    ],

    cmdclass = {
        'install': CustomInstallCommand,
    },

    author = "Adfinis SyGroup AG",
    author_email = "http://adfinis-sygroup.ch/contact",
    description = "Adfinis SyGroup SyRPC Services Library",
    license = "GNU Library or Lesser General Public License (LGPL)",
    long_description = """
Library to access and provide syrpc rabbitmq services.""",
    keywords = "adfinis-sygroup rpc",
    url = "http://adfinis-sygroup.ch",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: "
        "GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ]
)
