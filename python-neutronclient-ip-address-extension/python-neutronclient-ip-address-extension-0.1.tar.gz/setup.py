import setuptools

setuptools.setup(
    name="python-neutronclient-ip-address-extension",
    version="0.1",
    description=("Rackspace IP Address Resource Extension for python-"
                 "neutronclient"),
    long_description="",
    author="Rackspace",
    author_email="neutron-requests@lists.rackspace.com",
    url=("http://github.com/rackerlabs/"
         "python_neutronclient_ip_address_extension"),
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: OpenStack",
        "Programming Language :: Python"
    ],
    install_requires=["rackspace-python-neutronclient"],
    py_modules=["python_neutronclient_ip_address_extension"],
    entry_points={
        "neutronclient.extension": [
            "ip_address = python_neutronclient_ip_address_extension"]
    }
)
