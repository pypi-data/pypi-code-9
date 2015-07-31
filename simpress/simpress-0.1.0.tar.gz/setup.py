from setuptools import setup

setup(
    name='simpress',
    packages=['simpress'],
    entry_points={"console_scripts": ["press-init=simpress.commands:init"]},
    version='0.1.0',
    author='Ryo Miyake',
    author_email='ryo.studiom@gmail.com',
    description="Simple document system by GitHub flavored Markdown.",
    long_description=open('README.md').read(),
    url='http://github.com/nekoya/simpress',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
    ],
)
