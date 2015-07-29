from setuptools import setup, find_packages
setup(
    name = "restful.py",
    version = "1.0",
    packages = find_packages(),

    install_requires=['web.py>=0.37'],
    tests_require=['nose'],

    # metadata for upload to PyPI
    author='Damian Hagge',
    author_email = "damianhagge@gmail.com",
    description = "Python framework for rest services that adds content negotiation to web.py",
    license = "Apache Software License 2.0",
    keywords = "rest web.py webpy restful content negotiation",
    url='https://github.com/dhagge/restful.py/',
    extras_require={
        'testing': ['nose'],
    }
)