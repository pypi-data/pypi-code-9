import os
import sys
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

reqs = []
if [sys.version_info[0], sys.version_info[1]] < [2, 7]:
    reqs.append("simplejson>=2.0.9")

setup(
    name='django-datadog',
    version='1.0',
    packages=[
        'djdatadog',
        'djdatadog.middleware'
    ],
    include_package_data=True,
    license='BSD',
    description='simple Django middleware for submitting timings and exceptions to Datadog.',
    long_description=README,
    author='Chris Heisel',
    author_email='cheisel@kabbage.com',
    install_requires=reqs.extend([
        'datadog==0.4.0'
    ])
)
