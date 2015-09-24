from distutils.core import setup

# Read the version number
with open("json_scheming/_version.py") as f:
    exec(f.read())

setup(
    name='json_scheming',
    version=__version__, # use the same version that's in _version.py
    author='David N. Mashburn',
    author_email='david.n.mashburn@gmail.com',
    packages=['json_scheming'],
    scripts=[],
    url='http://pypi.python.org/pypi/json_scheming/',
    license='LICENSE.txt',
    description='Tools to build pseudo-schemas from json (and nested lists of dicts)',
    long_description=open('README.txt').read(),
    install_requires=[],
)
