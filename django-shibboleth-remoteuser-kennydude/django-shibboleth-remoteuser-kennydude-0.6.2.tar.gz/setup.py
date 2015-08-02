from setuptools import setup, find_packages

LONG_DESCRIPTION = ''
try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

setup(
    name='django-shibboleth-remoteuser-kennydude',
    version='0.6.2',
    description="Use Shibboleth users inside of Django",
    long_description=LONG_DESCRIPTION,
    author='Joe Simpson',
    author_email='me@kennydude.me',
    packages=find_packages(),
)
