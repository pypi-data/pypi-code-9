from setuptools import setup

setup(
    name='python-nebri-authentication',
    version='0.1.1',
    description="python-nebri-authentication is a simple and easy-to-use package to make authenticated nebri api requests from a python application.",
    packages=['nebri_auth'],
    url='http://github.com/briem-bixly/python-nebri-authentication/',
    author='briem-bixly',
    install_requires=[
        'python-nebri>=0.1.4'
    ],
)