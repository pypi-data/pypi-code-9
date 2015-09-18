from distutils.core import setup

setup(
    name='django-dajaxice-me',
    version='0.8',
    author='Jorge Bastida',
    author_email='me@jorgebastida.com',
    maintainer='Leopoldo Parra',
    maintainer_email='lparra.dev@gmail.com',
    description='Agnostic and easy to use ajax library for django',
    url='https://github.com/Leonime/django-dajaxice.git',
    license='BSD',
    packages=['dajaxice',
              'dajaxice.templatetags',
              'dajaxice.core'],
    package_data={'dajaxice': ['templates/dajaxice/*']},
    long_description=("Easy to use AJAX library for django, all the "
                      "presentation logic resides outside the views and "
                      "doesn't require any JS Framework. Dajaxice uses the "
                      "unobtrusive standard-compliant (W3C) XMLHttpRequest "
                      "1.0 object."
                      "This is a fork I made to add support for Django 1.8"
                      "and remove deprecation warnings."),
    install_requires=[
        'Django>=1.3'
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
