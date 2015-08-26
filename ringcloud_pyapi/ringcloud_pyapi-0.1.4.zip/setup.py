from setuptools import setup

import codecs

import ringcloud_pyapi


def read(filename):
    return codecs.open(filename, 'r', encoding='utf-8').read()

setup(
    name=ringcloud_pyapi.__title__,
    version=ringcloud_pyapi.__version__,
    description='RingCloud API Client',
    long_description=(read('README.rst')),
    url='https://bitbucket.org/ringcloud/ringcloud_pyapi',
    author=ringcloud_pyapi.__author__,
    author_email='devel@ringcloud.ru',
    packages=['ringcloud_pyapi'],
    keywords=['ringcloud', 'rest', 'api'],
    install_requires=["requests"],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license=ringcloud_pyapi.__license__
)
