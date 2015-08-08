from distutils.core import setup, Extension, Command
from distutils.command.build_ext import build_ext
import os
import os.path
import time
import glob
import sys
import shutil
import json
import re
from setuptools import setup
from distutils.core import setup
from distutils.extension import Extension


_python = 'python' if sys.version_info[0] < 3 else 'python3'


class _DocumentCommand(Command):
    user_options = [
        ('clean', 'c', 'clean'),
        ('aspell', 'a', 'run aspell')]

    def initialize_options(self):
        self._dir = os.getcwd()
        self.aspell = False
        self.clean = False

    def finalize_options(self):
        pass

    def run(self):
        try:            
            os.chdir('docs')

            os.system('gprof2dot ../test/data/gprof.txt | profile_eye > build/html/gprof.html')

            os.system('%s -m profile -o profile.pstats ../test/data/recipe-579047-1.py' % _python)
            os.system('gprof2dot -f pstats profile.pstats | profile_eye > build/html/recipe.html')
            os.system('gprof2dot -f pstats profile.pstats | profile_eye --file-colon-line-colon-label-format > build/html/recipe_colon.html')

            if self.clean:
                os.system('make clean')

            os.system('make html')
            os.system('cp -r ../profile_eye/_js build/html/_js')
            
            if self.aspell:
                for f_name in glob.iglob('*.html'):
                    os.system('aspell check %s' % f_name)
        finally:        
            os.chdir('..')


class _TestCommand(Command):
    user_options = [ 
        ('which=', None, 'Specify the test to run.')
        ]

    def initialize_options(self):
        self.which = None

    def finalize_options(self):
        if self.which is None:
            self.which = ''

    def run(self):
        try:
            os.chdir('test')
            # TODO(AmiT)
            run_str = '%s __init__.py %s' % (_python, self.which)
            os.system(run_str)
        finally:        
            os.chdir('..')


setup(
    name='ProfileEye',
    version= re.search(
        "^__version__\s*=\s*'(.*)'",
        open('profile_eye/profile_eye.py').read(),
        re.M
        ).group(1),
    author='Ami Tavory, Qwilt',
    author_email='amit@qwilt.com',
    packages=[
        'profile_eye'],
    zip_safe = False,
    entry_points = {
        "console_scripts": ['profile_eye = profile_eye.profile_eye:main']
        },    
    package_data = {
        'profile_eye': [
            '_js/*.js', 
            '_tmpl/*.*']
    },
    license='BSD',
    description='A browser-based visualization frontend for gprof2dot',
    long_description=open('README.txt').read(),
    requires=[
        'setuptools',
        'six',
        'gprof2dot',
        'jinja2'],
    cmdclass={ 
        'test': _TestCommand, 
        'document': _DocumentCommand},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',   
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'])




