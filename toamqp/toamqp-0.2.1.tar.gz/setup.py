import distutils.core
import os
import sys

try:
    # to enable "python setup.py develop"
    import setuptools
except ImportError:
    pass

from stormed.version import __VERSION__

KEYWORDS = ['tornado', 'amqp', 'tornado amqp']

DESCRIPTION = ('native tornadoweb amqp 0-9-1 client implementation. '
               'Forked From https://github.com/paolo-losi/stormed-amqp/')


def _setup():
    distutils.core.setup(
        name='toamqp',
        version=__VERSION__,
        description=DESCRIPTION,
        keywords=KEYWORDS,
        author='ZY ZHANG',
        author_email='idup2x@gmail.com',
        url="http://github.com/bufferx/stormed-amqp/",
        license="http://www.opensource.org/licenses/mit-license.html",
        packages = ["stormed", "stormed.method", "stormed.method.codegen"],
        install_requires=['tornado'],
    )


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('make publish')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            assert type_ in ('major', 'minor', 'patch')

            os.system('bumpversion --current-version {} {}'
                      .format(__VERSION__, type_))
            sys.exit()

    _setup()


if __name__ == '__main__':
    main()
