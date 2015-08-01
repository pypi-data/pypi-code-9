import setuptools

setuptools.setup(
    name="ohh",
    version="0.6.0",
    url="https://git.claudetech.com/ohh/ohh-cli",

    author="Daniel Perez",
    author_email="daniel@claudetech.com",

    description="CLI tool for OHH project",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    scripts=['bin/ohh'],

    install_requires=[
        'requests',
        'psutil',
        'python-dateutil',
        'pync',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
