from distutils.core import setup

setup(
    name='PyStrawpoll',
    version='0.1.4',
    author='Vaibhav Yenamandra',
    author_email='vaibhav-y@users.noreply.github.com',
    packages=['strawpoll', 'tests'],
    url='http://pypi.python.org/pypi/PyStrawpoll/',
    license='LICENSE.txt',
    description='Python API wrapper for strawpoll (https://github.com/vaibhav-y/py-strawpoll)',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests >= 2.4.1"
    ]
)
