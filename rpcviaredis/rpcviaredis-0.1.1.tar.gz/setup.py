from setuptools import setup, find_packages

setup(
    name="rpcviaredis",
    py_modules=['rpcviaredis'],
    version=open('VERSION', 'rt').read(),
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author="Oscar LASM",
    author_email="lasm.landry@gmail.com",
    keywords=['Redis','RPC'],
    description="Build RPC pattern via redis connection",
    long_description=open('README.md', 'rt').read(),
    install_requires=['redis>=2.10.3'],
    extras_require = {'msgpack': 'msgpack-python'},
    include_package_data=True,
    url='https://github.com/moas/rpcviaredis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
	    'Topic :: System :: Distributed Computing'
    ],
    license="GNU V2.0",
)
