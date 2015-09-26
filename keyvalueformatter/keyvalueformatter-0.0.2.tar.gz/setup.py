try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()

requirements = [
    "six",
]

test_requirements = [
    "nose",
    "mock",
    "testfixtures",
]

setup(
    name='keyvalueformatter',
    version='0.0.2',
    description='Allows easy key=value formatting for standard python logging',
    long_description=readme,
    author='Kyle James Walker',
    author_email='KyleJamesWalker@gmail.com',
    url='https://github.com/KyleJamesWalker/keyvalueformatter',
    packages=['keyvalueformatter'],
    package_dir={'keyvalueformatter':
                 'keyvalueformatter'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
