import re

from setuptools import setup

# Fetch version number from the client init file.
version = None
for line in open('./imagefy/__init__.py'):
    m = re.search('__version__\s*=\s*(.*)', line)
    if m:
        version = m.group(1).strip()[1:-1]  # Quotes
        break
assert version

setup(
    name='imagefy',
    version=version,
    description='A Python wrapper for the Imagefy API.',
    author='Atte Valtonen',
    author_email='atte.valtonen@sin.ga',
    url='https://bitbucket.org/singster/imagefy-sdk-python',
    license='MIT',
    packages=['imagefy'],
    include_package_data=False,
    use_2to3=False,
    install_requires=[
        'aniso8601>=1.0.0',
        'requests>=2.4',
    ]
)
