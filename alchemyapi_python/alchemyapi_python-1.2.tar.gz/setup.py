from setuptools import setup

setup(
    name='alchemyapi_python',
    version='1.2',
    packages=['alchemyapi'],
    url='https://github.com/AlchemyAPI/alchemyapi_python',
    license='Apache',
    author='AlchemyAPI',
    author_email='support@alchemyapi.com',
    description='Enhanced version of AlchemyAPI Python SDK',
    long_description=open('README.md', 'r').read(),
    install_requires=['requests'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
