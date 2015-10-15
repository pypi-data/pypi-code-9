from setuptools import setup


setup(
    name='django-nimda',
    version='0.0.1',
    description='A light weight attempt at spicing up the django admin',
    long_description=open('README.rst').read(),
    author='AIno',
    author_email='hello@aino.com',
    url='http://github.com/aino/django-nimda',
    packages=['nimda'],
    include_package_data=True,
    install_requires=['Django>=1.8'],
    license='ICS',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    zip_safe=False
)
