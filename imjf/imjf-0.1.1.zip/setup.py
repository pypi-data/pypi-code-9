from distutils.core import setup

version = '0.1.1'

setup(
    name='imjf',
    packages=['imjf'],
    version=version,
    description='The official Python client for www.isMyJsFucked.com',
    author='Drew French',
    author_email='rectangletangle@gmail.com',
    url='https://github.com/rectangletangle/imjf-py',
    download_url='https://github.com/rectangletangle/imjf-py/tarball/{version}'.format(version=version),
    install_requires=['requests']
)
