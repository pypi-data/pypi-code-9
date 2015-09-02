try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import cmsplugin_oembed

version = cmsplugin_oembed.__version__

setup(
    name = 'cmsplugin_oembed',
    packages = ['cmsplugin_oembed'],
    include_package_data = True,
    version = version,
    description = "Responsive video embedding for djangocms",
    author = 'Christoph Reimers',
    author_email = 'creimers@byteyard.de',
    license='BSD License',
    url = 'https://github.com/byteyard/djangocms_oembed',
    keywords = ['djangocms', 'django', 'responsive', 'oembed', 'video'], 
    install_requires = [
        'django-cms>=3.0',
        'django-embed-video==1.0.0',
        'django-sekizai>=0.8',
    ],
    classifiers = [
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
