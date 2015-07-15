from setuptools import setup

setup(
    name='x100idgen',
    version='0.1.8',

    description='Id generator require no centralized authority',
    long_description=open('README.rst').read(),
    url='https://github.com/chengang/x100idgen',
    author='Chen Gang',
    author_email='yikuyiku.com@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='uuid idgen id IdGenerator x100',

    py_modules=['x100idgen'],
    test_suite='tests',
)
