#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A deployer, remote shell and status monitor built upon MarcoPolo
"""

from setuptools import setup, find_packages
from distutils.command.clean import clean
from distutils.command.install import install
from codecs import open
import os, sys, subprocess
import glob
import stat

custom_deployer_params = [
                            "--marcodeployer-disable-daemons",
                            "--marcodeployer-disable-deployer",
                            "--marcodeployer-enable-receiver",
                            "--marcodeployer-no-start"
                         ]

def detect_init():
    try:
        subprocess.check_call(["systemctl", "--version"], stdout=None, stderr=None, shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1

def enable_service(service):
    sys.stdout.write("Enabling service " + service +"...\n")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!\n")

def start_service(service):
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "stop", service], shell=False)
        subprocess.call(["systemctl", "start", service], shell=False)
    else: 
        subprocess.call(["service", service, "stop"], shell=False)
        subprocess.call(["service", service, "start"], shell=False)

    sys.stdout.write("Started!\n")

if __name__ == "__main__":

    deployer_params = []

    python_version = int(sys.version[0])

    for param in sys.argv:
        if param in custom_deployer_params:
            deployer_params.append(param)
            sys.argv.remove(param)

    here = os.path.abspath(os.path.dirname(__file__))

    long_description = ""
    
    with open(os.path.join(here, "DESCRIPTION.rst"), encoding='utf-8') as f:
        long_description = f.read()

    def copy_dir(directory, module):
        dir_path = directory
        base_dir = os.path.join(module, dir_path)
        for (dirpath, dirnames, files) in os.walk(base_dir):
            for f in files:
                yield os.path.join(dirpath.split('/', 1)[1], f)

    data_files = [
                    ('/usr/lib/marcodeployer/static/css', glob.glob("usr/lib/marcodeployer/static/css/*")),
                    ('/usr/lib/marcodeployer/static/fonts', glob.glob("usr/lib/marcodeployer/static/fonts/*")),
                    ('/usr/lib/marcodeployer/static/img',  glob.glob("usr/lib/marcodeployer/static/img/*")),
                    ('/usr/lib/marcodeployer/static/js',  glob.glob("usr/lib/marcodeployer/static/js/*")),
                    ('/usr/lib/marcodeployer/certs', glob.glob("usr/lib/marcodeployer/certs/*")),
                    ('/usr/lib/marcodeployer/templates', glob.glob("usr/lib/marcodeployer/templates/*.jade")),
                    ('/etc/marcodeployer', glob.glob('etc/marcodeployer/*'))
                 ]
    
    daemon_files = []
    if "--marcodeployer-disable-daemons" not in deployer_params:
        init_bin = detect_init()

        if init_bin == 1:
            daemon_files = [
                            ('/etc/init.d/', ["daemon/systemv/marcodeployerd", 
                                              "daemon/systemv/marcoreceiverd"])
                            ]

        else:
            daemon_files = [
                            ('/etc/systemd/system/', ["daemon/systemd/marcodeployerd.service", 
                                                      "daemon/systemd/marcoreceiverd.service"])
                           ]

    data_files.extend(daemon_files)

    description = "The deployer for the marcopolo environment"

    setup(
        name="marcopolo-deployer",
        provides=["marcodeployer"],
        version='0.1.6',
        description=description,
        long_description = long_description,
        url="marcopolo.martinarroyo.net/apps/marcodeployer",
        author="Diego Martín",
        author_email="martinarroyo@usal.es",
        license="MIT",
        classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',

        ],
        keywords="marcopolo deployer statusmonitor",
        packages=find_packages(),
        install_requires=[
            'certifi>=2015.4.28',
            'netifaces>=0.10.4',
            'pyjade>=3.0.0',
            'python-pam>=1.8.2',
            'requests>=2.7.0',
            'requests-futures>=0.9.5',
            'six>=1.9.0',
            'tornado>=4.1',
            'marcopolo>=0.1.0',
            'marcopolo.bindings>=0.1.0',
        #    'transifex-client',
        #    'sphinx-intl'
        ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
            'console_scripts':[
                'marcodeployerd = marcodeployer.deployer:main',
                'marcoreceiverd = marcodeployer.receiver:main'
            ]
        }
    )

    if "install" in sys.argv:
        if "--marcodeployer-disable-daemons" not in deployer_params:
            if "--marcodeployer-disable-deployer" not in deployer_params:
                enable_service("marcodeployerd")
                if "--marcodeployer-no-start" not in deployer_params:
                    start_service("marcodeployerd")

            if "--marcodeployer-enable-receiver" in deployer_params:
                enable_service("marcoreceiverd")
                if "--marcodeployer-no-start" not in deployer_params:
                    start_service("marcoreceiverd")

        if not os.path.exists("/var/log/marcodeployer"):
            os.makedirs('/var/log/marcodeployer')

        for f in os.listdir('/usr/lib/marcodeployer/certs'):
            os.chmod(os.path.join('/usr/lib/marcodeployer/certs', f), stat.S_IREAD | stat.S_IWRITE)

        os.chmod('/etc/marcodeployer/secret', stat.S_IREAD | stat.S_IWRITE)