from distutils.core import setup

setup(
    name='AMP',
    version='1.0.0.0',
    author='Ini Oguntola',
    author_email='ioguntol@gmail.com',
    packages=['AMP'],
    scripts=[],
    url='http://github.com/ioguntol/Automatic-Mathematical-Parser/',
    license='LICENSE.txt',
    description='Automatic Mathematical Parser.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
        "caldav == 0.1.4",
    ],
)
