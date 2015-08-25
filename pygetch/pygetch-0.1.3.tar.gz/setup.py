from distutils.core import setup

setup(
    name='pygetch',
    version='0.1.3',
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    packages=[
        'pygetch',
        'pygetch.getch',
        'pygetch.settings',
        'pygetch.utils',
        'pygetch.test',
    ],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/pygetch/',
    license='LICENSE.txt',
    description='Pure-Python, standard-library, platform-independent getch utils.',
    long_description=open('README').read(),
    install_requires=[],
)
