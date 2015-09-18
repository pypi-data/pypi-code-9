from distutils.core import setup

setup(
    name='django-dajax-me',
    version='0.9.4',
    author='Jorge Bastida',
    author_email='me@jorgebastida.com',
    maintainer='Leopoldo Parra',
    maintainer_email='lparra.dev@gmail.com',
    description=('Easy to use library to create asynchronous presentation '
                 'logic with django and dajaxice'),
    url='https://github.com/Leonime/django-dajax.git',
    download_url='https://github.com/Leonime/django-dajax/tarball/0.9.3',
    license='BSD',
    packages=['dajax'],
    package_data={'dajax': ['static/dajax/*']},
    long_description=('dajax is a powerful tool to easily and super-quickly '
                      'develop asynchronous presentation logic in web '
                      'applications using python and almost no JS code. It '
                      'supports up to four of the most popular JS frameworks: '
                      'jQuery, Prototype, Dojo and mootols.'
                      'This is a fork I made to add support for Django 1.8'),
    install_requires=[
        'django-dajaxice-me>=0.8'
    ],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities']
)
