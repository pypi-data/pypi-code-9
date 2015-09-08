from setuptools import setup

setup(
    name='toka',
    version='0.2.3.21',
    keywords=('handy tool', 'common files'),
    description='A handy tool to generate common files in command line',
    license='MIT License',
    author='fenjuly',
    author_email='newfenjuly@gmail.com',

    install_requires=[],
    packages=['tokapy'],
    package_dir={'tokapy': 'tokapy'},
    package_data={'tokapy': ['lib/gitignore/*.gitignore', 'lib/license/*', 'lib/webpack/*.js'],},
    entry_points={
        'console_scripts': [
            'toka = tokapy.toka:main',
        ],
    },
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)