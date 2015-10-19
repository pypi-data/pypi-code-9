from setuptools import setup, find_packages


setup(
    name="django-unihandecodejs",
    version="0.1.0",
    url='https://github.com/georgema1982/django-unihandecode',
    license='GPLv3/Perl',
    description="A Django app that simply provides unihandecode.js (https://github.com/ojii/unihandecode.js) out of box to be used along side with Django CMS.",
    long_description=open('README.rst').read(),
    author='George Ma',
    author_email='george.ma1982@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
)
