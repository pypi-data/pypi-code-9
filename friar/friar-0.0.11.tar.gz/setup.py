from setuptools import setup, find_packages

__VERSION__ = '0.0.11'

setup(
    name='friar',
    version=__VERSION__,
    description='A simple Python wrapper for jsonrpc interfaces',
    long_description='A simple Python wrapper for jsonrpc interfaces',
    url='http://jameselford.com/friar',
    author='James Elford',
    author_email='james.p.elford@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='jsonrpc, client',

    packages=find_packages(exclude=['test*']),
    install_requires=['requests'],
    tests_require=[],
)
