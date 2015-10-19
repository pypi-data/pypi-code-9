from distutils.core import setup
setup(
    name = 'django_nvd',
    packages = ['django_nvd'], # this must be the same as the name above
    version = '0.0.2',
    description = 'A Django app with models for storing the NVD information',
    author = 'Daniel Vaca',
    author_email = 'daniel.vaca.araujo@gmail.com',
    url = 'https://github.com/diviei/django_nvd', # use the URL to the github repo
    download_url = 'https://github.com/diviei/django_nvd/tarball/0.0.1', # I'll explain this in a second
    keywords = ['nvd', 'cve', 'django', 'vulnerabilities'], # arbitrary keywords
    classifiers = [],
)