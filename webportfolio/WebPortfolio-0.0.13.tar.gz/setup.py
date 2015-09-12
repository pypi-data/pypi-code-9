"""
Web-Portfolio

Web-Portfolio is a Flask based framework to help quickly develop web applications, by
adding structure to your views and templates.

Philosophy:

To create a framework that runs everywhere, regardless of the platform, by
providing cloud balh...

It made the following decisions for you: (of course you can change them)


It comes with pre-built components:


And it is still Flask.



Portfolio is a framework based on Flask extension that adds structure to both your views and
templates, by mapping them to each other to provide a rapid application development framework.
The extension also comes with Flask-Classy, Flask-Assets, Flask-Mail,
JQuery 2.x, Bootstrap 3.x, Font-Awesome, Bootswatch templates.
The extension also provides pre-made templates for error pages and macros.

http://pylot.io/
https://github.com/mardix/web-portfolio

"""

import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

__about__ = {}
with open(os.path.join(base_dir, "webportfolio", "__about__.py")) as f:
    exec(f.read(), __about__)

setup(
    name=__about__["title"],
    version=__about__["version"],
    license=__about__["license"],
    author=__about__["author"],
    author_email=__about__["email"],
    description=__about__["description"],
    url=__about__["uri"],
    long_description=__doc__,
    py_modules=['webportfolio'],
    entry_points=dict(console_scripts=[
        'webportfolio=webportfolio.cli:cli',
        'wp=webportfolio.cli:cli',
    ]),
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'Flask==0.10.1',
        'Flask-Classy==0.6.10',
        'Flask-Assets==0.10',
        'flask-recaptcha==0.4.1',
        'flask-login==0.3.0',
        'flask-kvsession==0.6.1',
        'flask-s3==0.1.7',
        'flask-mail==0.9.0',
        'flask-cache==0.13.1',
        'flask-cloudy==0.12.0',
        'flask-seasurf==0.2.0',

        'Active-Alchemy==0.4.4',
        'Paginator==0.3.5',
        'authomatic==0.1.0.post1',
        'six==1.9.0',
        'passlib==1.6.2',
        'bcrypt==1.1.1',
        'python-slugify==0.1.0',
        'humanize==0.5.1',
        'redis==2.9.1',
        'ses-mailer==0.12.1',
        'markdown==2.6.2',
        'inflection==0.3.1',
        'pyyaml==3.11',
        'click==5.1'
    ],
    dependency_links=[
        'https://github.com/maxcountryman/flask-login/archive/4d439e8050a8ee942cb76a0309faec9202b8aca9.zip#egg=flask-login-0.3.0'
    ],
    keywords=['flask',
              'portfolio',
              'templates',
              'views',
              'classy',
              'framework',
              "mvc",
              "blueprint",
              "webportfolio"],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

