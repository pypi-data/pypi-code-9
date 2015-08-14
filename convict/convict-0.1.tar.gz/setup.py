from setuptools import setup, find_packages

setup(
    name="convict",
    version="0.1",
    description="python clone of node-convict " +
    "(https://github.com/mozilla/node-convict)",
    author="Daniel Thornton",
    author_email="daniel@relud.com",
    include_package_data=True,
    license='MPL 2.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        # currently only tested in python 2.7
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
