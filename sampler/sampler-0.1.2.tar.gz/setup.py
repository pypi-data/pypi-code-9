from setuptools import setup

setup(
    name='sampler',
    version='0.1.2',
    description='Sample data generator for Python',
    keywords='sampler test data generator',
    url='https://github.com/hyperborea/python-sampler.git',
    author='Sven Perkmann',
    author_email='sven.perkmann@gmail.com',
    license='MIT',
    packages=['sampler'],
    install_requires=['fake-factory'],
)