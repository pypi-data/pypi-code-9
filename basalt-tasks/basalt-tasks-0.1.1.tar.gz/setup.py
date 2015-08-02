from setuptools import setup, find_packages

setup(
    name='basalt-tasks',
    version='0.1.1',
    packages=find_packages("."),
    include_package_data=True,
    url='https://github.com/basalt/python-basalt',
    license='MIT',
    author='Jochen Breuer',
    author_email='brejoc@gmail.com',
    install_requires=[
        'invoke==0.7.0',
        'PyYAML',
        'Jinja2',
        'sh',
    ],
    description='Helper functions for the basalt invoke build file.',
    platforms='any',
)
