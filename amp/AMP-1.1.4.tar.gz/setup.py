from distutils.core import setup

setup(
    name='AMP',
    version='1.1.4',
    author='Ini Oguntola',
    author_email='ioguntol@gmail.com',
    packages=['AMP', 'AMP.test'],
    scripts=[],
    url='http://github.com/ioguntol/amp/',
    license='LICENSE.txt',
    description='A Python 2.7 mathematical parsing library',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
        "caldav == 0.1.4",
    ],
)
