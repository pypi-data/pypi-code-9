from distutils.core import setup


setup(
    name = 'djangorcp',
    packages = [
        'djangorcp'
    ],
    package_data={'': ['static/djangorcp/*']},
    version = '1.0.16',
    description = 'A color picker field for Django admin that lets you pick a color from 24 randomly generated colors.',
    author = 'Johan Frisell',
    author_email = 'johan@trell.se',
    requires = [
        'Django (>=1.7)',
    ],
    url = 'https://github.com/frisellcpl/django-random-color-picker-field',
    download_url = 'https://github.com/frisellcpl/django-random-color-picker-field/tarball/1.0.16',
    keywords = [
        'django',
        'colorpicker',
        'django admin',
        'color picker'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
