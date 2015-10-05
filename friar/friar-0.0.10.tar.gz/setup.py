from setuptools import setup, find_packages

__VERSION__ = '0.0.10'

setup(
    name='friar',
    version=__VERSION__,
    description='A simple library for working with jsonrpc apis',
    long_description='A simple library for working with jsonrpc apis',
    url='http://jsonrpcclient.jameselford.com',
    author='James Elford',
    author_email='james.p.elford@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='jsonrpc',

    packages=find_packages(exclude=['test*']),
    install_requires=['requests'],
    tests_require=[],
)
