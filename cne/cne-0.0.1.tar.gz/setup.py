from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='cne',
    version='0.0.1',
    description='Get fuel price from cne api',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cne fuel api',
    url='http://github.com/lgaticaq/python-cne',
    author='Leonardo Gatica',
    author_email='lgatica@protonmail.com',
    license='MIT',
    packages=['cne'],
    install_requires=[
        'requests',
        'pydash',
    ],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
