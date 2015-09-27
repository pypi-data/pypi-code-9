#!/usr/bin/env python

name = 'mux-twitter'
path = 'mux'


## Automatically determine project version ##
from setuptools import setup, find_packages
try:
    from hgdistver import get_version
except ImportError:
    def get_version():
        import os
        
        d = {'__name__':name}

        # handle single file modules
        if os.path.isdir(path):
            module_path = os.path.join(path, '__init__.py')
        else:
            module_path = path
                                                
        with open(module_path) as f:
            try:
                exec(f.read(), None, d)
            except:
                pass

        return d.get("__version__", 0.1)

## Use py.test for "setup.py test" command ##
from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


## Try and extract a long description ##
readme = ""
for readme_name in ("README", "README.rst", "README.md",
                    "CHANGELOG", "CHANGELOG.rst", "CHANGELOG.md"):
    try:
        readme += open(readme_name).read() + "\n\n"
    except (OSError, IOError):
        continue


## Finally call setup ##
setup(
    name = name,
    version = get_version(),
    packages = find_packages(),
    author = "Da_Blitz",
    author_email = "code@pocketnix.org",
    maintainer=None,
    maintainer_email=None,
    description = "CLI twitter client using the streaming API",
    long_description = readme,
    license = "MIT BSD",
    keywords = "twitter streaming asyncio client",
    download_url="http://blitz.works/mux/archive/tip.zip",
    classifiers=[
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: POSIX :: Linux",
                 "Programming Language :: Python :: 3",
                 "Topic :: Communications",
                 "Topic :: Internet",
                ],
    platforms=None,
    url = "http://blitz.works/mux/",
    test_loader = "pytest:tests",
    test_suite = "all",

    entry_points = {"console_scripts":[
                        "mux-stream = mux.cmdline:stream_main",
                        "mux = mux.cmdline:cli_main",],
                   },
    zip_safe = True,
    setup_requires = ['hgdistver'],
    install_requires = ['PyYAML>=3.11', 
                        'requests>=2.3.0', 
                        'twython>=3.2.0', 
                        'Delorean>=0.4.5', 
                        'butter>=0.9.2', 
                        'appdirs',
                        'blessed',
                        ],
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
