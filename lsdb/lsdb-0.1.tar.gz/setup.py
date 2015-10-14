__author__ = 'donb'


# from setuptools import setup

"""
setup(
    name='yourscript',
    version='0.1',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourscript:cli
    ''',
)
"""

from setuptools import setup, find_packages

setup(
    name='lsdb',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],

    author='Don Brotemarkle',
    author_email='donbro@mac.com',

    license='Apache Software License',

    description='swiss-army-knife for filesystem metadata to database',

    classifiers = [

        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],

    entry_points='''
        [console_scripts]
        lsdb=lsdb.scripts.lsdb_cli:cli
    ''',
)