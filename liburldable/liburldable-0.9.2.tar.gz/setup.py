from distutils.core import setup

setup(
    name='liburldable',
    version='0.9.2',
    author='hvm',
    author_email='hvm2hvm@gmail.com',
    packages=['liburldable'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    scripts=[],
    url='http://blog.voicuhodrea.com',
    license='LICENSE.txt',
    description='Urldable logic',
    long_description=open('README.txt').read(),
    install_requires=[
        # "Django >= 1.1.1", # just an example
    ],
)
