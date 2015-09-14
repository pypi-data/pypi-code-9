from setuptools import setup, find_packages

setup(
    name='turpial-sessions',
    version=str(1.0),
    description="turpial-sessions",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords='sessions,password,reset,django,turpial',
    author='turpial',
    author_email='lpimentel@turpialdev.com',
    url='',
    license='BSD',
    test_suite='',
    install_requires = [
        "django-bootstrap-form"
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
