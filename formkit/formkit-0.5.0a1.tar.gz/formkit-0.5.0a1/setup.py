from setuptools import setup


setup(**{
    'name':             'formkit',
    'version':          '0.5.0a1',
    'description':      'A kit for rapid development of powerful input forms.',
    'maintainer':       'MagicStack Inc.',
    'maintainer_email': 'hello@magic.io',
    'platforms':        ['any'],

    'include_package_data': True,
    'exclude_package_data': {
        '': ['.gitignore']
    },

    'classifiers': [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5'
    ]
})
