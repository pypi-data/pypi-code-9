from distutils.core import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='PyStrawpoll',
    version='0.1.2',
    author='Vaibhav Yenamandra',
    author_email='vaibhav-y@users.noreply.github.com',
    packages=['strawpoll', 'tests'],
    url='http://pypi.python.org/pypi/PyStrawpoll/',
    license='LICENSE.txt',
    description='Python API wrapper for strawpoll (https://github.com/vaibhav-y/py-strawpoll)',
    long_description=read_md('README.md'),
    install_requires=[
        "requests >= 2.4.1"
    ]
)
