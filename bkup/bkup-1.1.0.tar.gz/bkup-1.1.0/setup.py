from setuptools import setup, find_packages

setup(
    name='bkup',
    version='1.1.0',
    description='easily backup directories',
    url='https://github.com/ftzeng/bkup',
    author='Francis Tseng (@frnsys)',
    license='MIT',

    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        bkup=bkup:bkup
    ''',
)
