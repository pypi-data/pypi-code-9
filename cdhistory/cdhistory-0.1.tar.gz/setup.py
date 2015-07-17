#!/usr/bin/env python

import setuptools


setuptools.setup(
        name='cdhistory',
        version='0.1',
        description='Search for frequently visited directories',
        license='MIT',
        long_description=(open('README.md').read()),
        author='Joshua Downer',
        author_email='joshua.downer@gmail.com',
        url='http://github.com/jdowner/cdhistory',
        keywords='cd directory history alias search ',
        packages=['cdhistory'],
        package_data={
          '': ['share/*', '*.md', 'LICENSE'],
        },
        data_files=[
          ('share/cdhistory/', [
              'README.md',
              'LICENSE',
              'share/cdhistory.bash',
              ]),
        ],
        scripts=['bin/cdhistory'],
        install_requires=[
            'pep8',
            'tox',
            ],
        platforms=['Unix'],
        test_suite="tests",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Utilities',
            ]
        )
