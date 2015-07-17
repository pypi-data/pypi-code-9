#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The marco-bootstrap slave
"""
from setuptools import setup, find_packages
from codecs import open
import os, subprocess, glob, sys


from distutils.command.clean import clean
from distutils.command.install import install
import stat

custom_marcobootstrap_backend_params = [
                                    "--marcobootstrap-no-daemons",
                                    "--marcobootstrap-no-start",]


def detect_init():
    """
    Detects the daemon management tool used in the system
    """
    try:
        subprocess.check_call(["systemctl", "--version"], 
                               stdout=None, 
                               stderr=None, 
                               shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1


init_bin = detect_init()


def enable_service(service):
    sys.stdout.write("Enabling service "+service+"...")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!\n")

def start_service(service):
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "start", service], shell=False)
    else:
        subprocess.call(["service", service, "start"], shell=False)

    sys.stdout.write("Started!\n")

def set_cert_permissions():
    
    for cert in os.listdir("/etc/marcobootstrap/slave/certs"):
        os.chmod(os.path.join("/etc/marcobootstrap/slave/certs", cert), 
            stat.S_IREAD | stat.S_IWRITE)

    os.chmod("/etc/marcobootstrap/slave/certs", 
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

if __name__ == "__main__":
    marcobootstrap_params = []

    python_version = int(sys.version[0])

    marcobootstrap_params = [param for param in sys.argv\
                             if param in custom_marcobootstrap_backend_params]
    sys.argv = [arg for arg in sys.argv if arg not in marcobootstrap_params]

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()

    data_files = [
                  ("/etc/marcobootstrap/slave", ["etc/marcobootstrap/slave/slave.cfg"]),
                 ]
                 
    cert_files = [
                  ('/etc/marcobootstrap/slave/certs', 
                    glob.glob("etc/marcobootstrap/slave/certs/*"))
                 ]
    #bootcode_files = [('/etc/marcobootstrap/', ["etc/marcobootstrap/code.zip"])]

    if "--marcobootstrap-no-daemons" not in marcobootstrap_params:
        daemon_path = "daemon/"

        if init_bin == 1:
            daemon_files = [
                             ('/etc/init.d', 
                                [os.path.join(daemon_path, 
                                    "systemv/mbootstrapslad")])
                           ]
        else:
            daemon_files = [
                            ('/etc/systemd/system', 
                                [os.path.join(daemon_path, 
                                "systemd/mbootstrapslad.service")])
                           ]

        data_files.extend(daemon_files)
        data_files.extend(cert_files)
        #data_files.extend(bootcode_files)

    setup(
        name="marcobootstrap.slave",
        provides=["marcobootstrap.slave"],
        namespace_packages=["marcobootstrap"],
        version='0.0.18',
        description="The marcobootstrap slave",
        long_description=long_description,
        url="marcopolo.martinarroyo.net",
        author="Diego Martín",
        author_email="martinarroyo@usal.es",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Topic :: System :: Boot',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',

            'Intended Audience :: System Administrators',

            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

            'Natural Language :: English',
        ],
        keywords="polousers pxe ldap",
        packages=find_packages(),
        install_requires=[
            "requests>=2.7.0",
            "requests-futures>=0.9.5",
            "six>=1.9.0",
            "tornado>=4.1",
            "marcopolo>=0.0.1",
            "marcopolo.bindings>=0.0.1"
        ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
        'console_scripts':['mbootstrapslad = marcobootstrap.slave.slave:main']
        }

    )

    if "install" in sys.argv:
        set_cert_permissions()

        if "--marcobootstrap-no-daemons" not in marcobootstrap_params:
            enable_service("mbootstrapslad")
            if "--marcobootstrap-no-start" not in marcobootstrap_params:
                start_service("mbootstrapslad")

        if not os.path.exists("/var/log/marcopolo"):
            os.makedirs("/var/log/marcopolo")
