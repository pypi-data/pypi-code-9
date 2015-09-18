# coding: utf-8

from setuptools import setup

vcs_dependencies = [
    # This is a special fork where order_with_respect_to can be a tuple
    'git+https://github.com/lovasb/django-ordered-model.git#egg=django-ordered-model'
]

setup(
    name='django-yaat',
    version='1.3.0',
    packages=['yaat'],
    install_requires=['Django>=1.8.4', 'django-restify-framework==0.23', 'django-ordered-model'],
    include_package_data=True,
    dependency_links=vcs_dependencies,
    description='The django-restify-framework resource of the yaat AngularJs module',
    author='Slapec',
    url='https://github.com/slapec/django-yaat',
    license='MIT',
    zip_safe=False,
)
