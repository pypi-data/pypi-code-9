from setuptools import setup, find_packages

setup(
    name='SerialAlchemy',
    version='0.1.1-1',
    description='Simple object serialization for SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'SQLAlchemy',
        ],
    url='https://gitlab.com/sloat/SerialAlchemy',
    author='Matt Schmidt',
    author_email='matt@mattptr.net',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    )

