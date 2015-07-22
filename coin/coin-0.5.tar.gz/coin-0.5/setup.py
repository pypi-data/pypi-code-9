from setuptools import setup
from os.path import join, dirname

requirements = [
    'urllib3==1.7.1'
]

version = open(join(dirname(__file__), 'version')).read().strip()
print(version)

setup(
    name='coin',
    version=version,
    install_requires=requirements,
    scripts=['coin'],
    author='Syncloud',
    author_email='support@syncloud.it',
    url='https://github.com/syncloud/coin'
)