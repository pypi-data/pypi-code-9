from setuptools import setup, find_packages

setup(
    name='django-event-logger',
    version='0.8.15',
    packages=find_packages(),

    install_requires=['Django'],

    author='Brandon B.',
    author_email='unaffiliate@outlook.com',
    description='An easy-to-use event logger for Django.',
    keywords=['django', 'events', 'logger', 'logging'],
    url='https://github.com/receive/django-event-logger/',
    download_url='https://github.com/receive/django-event-logger/tarball/v0.8.15',
)
