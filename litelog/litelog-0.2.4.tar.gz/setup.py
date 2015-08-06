from distutils.core import setup

VERSION_FILE = 'version.txt'

VERSION = open(VERSION_FILE).read()

def next_version(version):
    """Increments the version given trivially"""
    nums = map(int, version.split('.'))
    (start, last) = nums[:-1], nums[-1]
    last += 1
    return '.'.join(map(str, start + [last]))

NEXT_VERSION = next_version(VERSION)


setup(
    name='litelog',
    version=VERSION,
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    py_modules=['litelog',],
    # scripts=[],
    url='http://pypi.python.org/pypi/litelog/',
    license='LICENSE.txt',
    description='Simplified, robust, selective, recursive logging utility for Python.',
    long_description=open('README.rst').read(),
    install_requires=[],
)


# increment dynamic working number
with open(VERSION_FILE, 'w') as FILE:
    FILE.write(NEXT_VERSION)
