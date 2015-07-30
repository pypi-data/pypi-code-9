import os
from setuptools import setup, find_packages
import calltoaction


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms-calltoaction',
    version=calltoaction.__version__,
    author='Sasha Matijasic',
    author_email='sasha@selectnull.com',
    packages=find_packages(),
    url='https://github.com/logithr/djangocms-calltoaction',
    license='MIT',
    description='djangocms plugin for managing lead generation calls to action',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        'django-cms>=3.1',
        'django-filer>=0.9.9',
        'cmsplugin-filer>=0.10',
        'django-parler>=1.4',
        'django-classy-tags>=0.60',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
