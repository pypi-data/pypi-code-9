from setuptools import find_packages, setup


version = '0.1.0'


install_requires={
    'django-pgcrypto-fields>=1.0.0,<2.0.0',
    'simplejson>=3.8.0,<4.0.0',
    'djangorestframework>=3.2.4,<4.0.0',
}


setup(
    name='django-model-logging',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='Generic and secure logging for changes to Django model instances',
    long_description=open('README.md').read(),
    author='Incuna',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-model-logging/',
    install_requires=install_requires,
    extras_require={},
    zip_safe=False,
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
    ],
)
