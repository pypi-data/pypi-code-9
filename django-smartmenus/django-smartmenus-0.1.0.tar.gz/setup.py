from setuptools import setup, find_packages


setup(
    name="django-smartmenus",
    version="0.1.0",
    url='https://github.com/georgema1982/django-smartmenus',
    license='MIT',
    description="A Django app that provides template tags to easily incorporate smartmenus.",
    long_description=open('README.rst').read(),
    author='George Ma',
    author_email='george.ma1982@gmail.com',
    packages=find_packages(exclude=['example*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
)
