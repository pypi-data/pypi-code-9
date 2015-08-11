from distutils.core import setup
setup(
    name = 'idalink',
    description = 'An interface to the insides of IDA!',
    version = '0.11',
    packages = ['idalink'],
    package_data = { 'idalink': [ 'support/*.sh' ] },
    install_requires=['rpyc']
)
