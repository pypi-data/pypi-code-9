from distutils.core import setup

setup(
    name='stretch',
    version='1.0',
    description='PBKDF2 on the command line',
    url='https://github.com/felipedau/stretch',
    author='Felipe Dau',
    author_email='dau.felipe@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security :: Cryptography',
    ],
    keywords='PBKDF2 key derivation function password stretching',
    scripts=[
        'stretch',
    ],
)
