from distutils.core import setup

setup(
    name='setupam',
    version='0.1.0',
    packages=['setupam'],
    url='https://github.com/gabrielaraujof/setupam',
    license='GPL v2',
    author='Gabriel Araujo',
    author_email='contato@gabrielaraujo.me',
    keywords=["encoding", "i18n", "xml"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

    description='Command-line tool to setup a speech corpus for CMU Sphinx.'
)
