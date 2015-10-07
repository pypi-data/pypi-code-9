from setuptools import setup, find_packages

setup(
    name='hufflepuff',
    version='1.0',
    description='Hufflepuffs are particularly good finders.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hufflepuff = hufflepuff.cli:main',
        ]
    },
)
