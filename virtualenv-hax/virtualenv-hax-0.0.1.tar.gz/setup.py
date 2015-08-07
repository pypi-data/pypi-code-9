from setuptools import setup

setup(
    name='virtualenv-hax',
    description='A wrapper around virtualenv that avoids sys.path sadness.',
    url='https://github.com/asottile/virtualenv-hax',
    version='0.0.1',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    py_modules=['virtualenv_hax'],
    install_requires=['argparse', 'virtualenv'],
    entry_points={
        'console_scripts': [
            'virtualenv-hax = virtualenv_hax:main',
        ],
    },
)
