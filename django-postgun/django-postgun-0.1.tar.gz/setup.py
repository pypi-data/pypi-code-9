import os
from setuptools import setup
 
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
 
# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setup(
    name = 'django-postgun',
    version = '0.1',
    packages = ['postgun'],
    install_requires = ["requests", "django"],
    include_package_data = True,
    license = 'BSD License',
    description = 'Send email using Mailgun with Mailgun specific attributes.',
    long_description = README,
    url = 'https://bitbucket.org/jamesvandyne/postgun',
    author = 'James Van Dyne',
    author_email = 'james@sugoisoft.com',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
        'Development Status :: 4 - Beta',
    ]
)