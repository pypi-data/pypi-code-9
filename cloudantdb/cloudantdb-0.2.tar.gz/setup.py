from setuptools import setup,find_packages
 
version = '0.2'
 
LONG_DESCRIPTION = """
=======================
CloudantDB
=======================

A declarative syntax Python ORM for Cloudant based on the official Cloudant Python library.

"""
 
setup(
    name='cloudantdb',
    version=version,
    description="""This project should make it easier for devs to use Cloudant with Python.""",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='cloudant, couchdb, django',
    author='Brian Jinwright',
    author_email='brian@ipoots.com',
    maintainer='Brian Jinwright',
    packages=find_packages(),
    
    license='Apache',
    install_requires=['cloudant>=0.5.9','lucene-querybuilder>=0.2'],
    include_package_data=True,
    zip_safe=False,
)
