# coding=utf8

"""
kks
---

Micro & Fast static blog generator (markdown => html). 4 - Beta

Features
````````

* Static: Markdown => HTML
* Not tags, No categories, No feed generation, No ...
* Minimal & Simple configuration
* Ability to run in the background as a daemon
* Ability to save posts in PDF for offline reading
* Ability to build automatically once source updated

Installation
`````````````

.. code:: bash

    $ mkdir MyBlog
    $ cd MyBlog
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    $ . venv/bin/activate
    $ pip install kks

Links
`````

* GitHub <https://github.com/kangkaisen/kks>
"""

from setuptools import setup, Extension


setup(
    name='kks',
    version='1.1.0',
    author='kangkaisen',
    author_email='kangkaisen@163.com',
    description='''a pithy and elegant python static blog''',
    license='BSD',
    keywords='static blog generator markdown, html',
    url='https://github.com/kangkaisen/kks/',
    packages=['kks'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'kks=kks.cli:main'
        ]
    },
    install_requires=open("requirements.txt").read().splitlines(),
    dependency_links=[
        'https://github.com/hit9/toml.py/zipball/master#egg=toml.py-0.1.2',
    ],
    ext_modules=[Extension('kkslibparser', ['src/libparser.c'])],
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ]
)
