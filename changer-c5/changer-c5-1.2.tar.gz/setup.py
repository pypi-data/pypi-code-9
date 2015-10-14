from setuptools import setup, find_packages
import os
import changer.c5

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='changer-c5',
    author='Christian Verkerk',
    author_email='christianverkerk@gmail.com',
    version=changer.c5.__version__,
    description='Changer C5 Component Library',
#    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='http://www.changer.nl',
    license='Private',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read().split(),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False
)
