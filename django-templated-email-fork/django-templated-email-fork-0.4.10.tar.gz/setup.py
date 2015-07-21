from setuptools import setup

DESCRIPTION = "A Django oriented templated / transaction email abstraction"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

setup(
    name='django-templated-email-fork',
    version='0.4.10',
    packages=['templated_email', 'templated_email.backends'],
    author='Andre Ericson',
    author_email='andre@vinta.com.br',
    url='https://github.com/vintasoftware/django-templated-email-fork',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
)
