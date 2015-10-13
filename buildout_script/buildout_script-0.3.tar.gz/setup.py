# Copyright (c) 2006-2015 Nathan R. Yergler, Creative Commons

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="buildout_script",
    version="0.3",

    packages=['buildout_script'],
    include_package_data=True,
    zip_safe=True,

    install_requires=[
        'setuptools',
        'zc.buildout',
    ],

    entry_points={
        'zc.buildout': [
            'default = buildout_script:Script',
            'template = buildout_script:Template',
        ],
    },

    author='Nathan R. Yergler',
    author_email='nathan@yergler.net',
    description='zc.buildout recipes for generating script and conf files '
        'from templates.',
    long_description=(
        read('README.rst')
        + '\n' +
        read('CHANGES.rst')
        + '\n' +
        'Download\n'
        '********\n'
    ),
    license='MIT License',
    url='https://github.com/nyergler/buildout_script',

    classifiers=[
        'Framework :: Buildout',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
