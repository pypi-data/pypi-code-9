
#!/usr/bin/env python
from setuptools import setup, find_packages

exec(open('kway/version.py').read())

setup(
    name='django-kway',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version=__version__,
    description='django-kway is an alternative to django gettext catalog with admin integration.',
    long_description=(
        'django-kway is an alternative to django gettext catalog and offers: '
        'i18n support (with multiple plural forms), django admin integration, '
        'kgettext function, ktrans template tag, caching, lazy modeltranslation integration and various settings.'
    ),
    author='Fabio Caccamo',
    author_email='fabio.caccamo@gmail.com',
    url='https://github.com/fabiocaccamo/django-kway',
    download_url='https://github.com/fabiocaccamo/django-kway/archive/%s.tar.gz' % __version__,
    keywords = ['django', 'admin', 'i18n', 'gettext', 'trans', 'alternative', 'key', 'modeltranslation', 'rosetta'],
    requires=['django(>=1.4)'],
    classifiers=[]
)

