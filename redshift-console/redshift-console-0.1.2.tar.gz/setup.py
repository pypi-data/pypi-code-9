import os

import pip
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        content = f.read()

    if paths[-1].endswith(".md"):
        try:
            import pypandoc
            content = pypandoc.convert(content, 'rst', format="md")
        except:
            print "Warning: pypandoc missing. Install it to convert text from Markdown to restructedText."

    return content

setup(
    name='redshift-console',
    version='0.1.2',
    description='Monitor and manage your Redshift cluster.',
    long_description=read('README.md'),
    url='http://github.com/EverythingMe/redshift_console/',
    license='Apache',
    author='Arik Fraimovich, Oren Itamar',
    author_email='opensource@everything.me',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[str(ir.req) for ir in install_reqs],
    entry_points = {
        'console_scripts': ['redshift-console=redshift_console.__main__:cli'],
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
)
