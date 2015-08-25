#-*- coding: utf8 -*-
import os
import setuptools
from setuptools import setup

VERSION = '0.1a0'
AUTHOR = 'Fábio Macêdo Mendes'

#
# Create meta.py file with updated version/author info
#
base, _ = os.path.split(__file__)
path = os.path.join(base, 'src', 'smallshapes', 'meta.py')
with open(path, 'w') as F:
    F.write(
        '# Auto-generated file. Please do not edit'
        '__version__ = %r\n' % VERSION +
        '__author__ = %r\n' % AUTHOR)

#
# Main configuration script
#
setup(
    name='smallshapes',
    version=VERSION,
    description='A simple engine that implements mathematical shapes of '
                'small dimensionality',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/fabiommendes/smallshapes',
    long_description=(
        r'''Simple mathematical shapes and geometrical operations in 2D, 3D
and low dimensions.
    
    * Implements AABB's, Circle and Convex Polygons.
    * TODO
    '''),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    license='GPL',
    requires=['smallvectors', 'six'],
)
