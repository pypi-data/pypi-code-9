import os
from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

packages = ['rest_sessions']

setup(
    name='django-rest-sessions',
    version='0.1.2',
    description= "Rest Session Backend For Django",
    long_description=read("README.rst"),
    keywords='django, sessions,',
    author='Hodur Sigurdor Heidarsson',
    author_email='hodur@temposoftware.com',
    url='https://stash.temposoftware.com/projects/TMC/repos/django-rest-sessions/browse',
    license='MIT',
    packages=packages,
    zip_safe=False,
    install_requires=['Django >= 1.8', 'requests>=2.7.0'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
