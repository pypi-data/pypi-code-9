from setuptools import setup

setup(
    name='foreman',
    packages=['foreman'],
    version='0.9.4',
    author='David Blaisonneau, Arnaud Morin',
    author_email='david.blaisonneau@orange.com, arnaud1.morin@orange.com',
    scripts=[],
    url='https://github.com/davidblaisonneau-orange/foreman',
    download_url='https://pypi.python.org/packages/source/F/Foreman/Foreman-0.9.3.tar.gz',
    license=open('LICENSE').read(),
    description='Python library to manipulate The Foreman through the API',
    long_description=open('README.rst').read(),
    install_requires=['requests-futures', 'requests'],
    keywords = ['foreman'],
)
