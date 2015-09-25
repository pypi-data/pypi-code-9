from setuptools import setup, find_packages
import os

PROJECT_DIR = os.path.dirname(__file__)

setup(
    name='django-email-username',
    version='0.0.3',
    packages=find_packages(),
    url='http://github.com/acordiner/django-email-username',
    license='GPL v2',
    author='Alister Cordiner',
    author_email='alister@cordiner.net',
    description='Use email addresses in place of usernames in Django projects.',
    long_description=open(os.path.join(PROJECT_DIR, 'README.rst')).read(),
    install_requires=[
        'django>=1.7,<1.9',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
