from distutils.core import setup

try:
    import pypandoc

    description = pypandoc.convert('../../README.md', 'rst')
except:
    description = ''

setup(
    name='SiRQL',
    version='0.0.1',
    packages=['sirql'],
    url='https://dev.flarecast.eu/stash/projects/DM/repos/sirql/browse',
    license='',
    author='Florian Bruggisser',
    author_email='florian.bruggisser@students.fhnw.ch',
    description='SiRQL is a simple language specification which defines the way how to receive and query data over an http request.',
    long_description=description,
    download_url='https://dev.flarecast.eu/stash/scm/dm/sirql.git',
    keywords=['sirql', 'request', 'language', 'simple', 'generic', 'query'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)
