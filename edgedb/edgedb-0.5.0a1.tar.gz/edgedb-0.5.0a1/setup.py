from setuptools import setup


setup(**{
    'name':             'edgedb',
    'version':          '0.5.0a1',
    'description':      'EdgeDB Python Binding',
    'maintainer':       'magicstack',
    'maintainer_email': 'info@edgedb.com',
    'url':              'http://edgedb.com',
    'platforms':        ['any'],

    'include_package_data': True,
    'exclude_package_data': {
        '': ['.gitignore']
    },

    'classifiers': [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5'
    ]
})
