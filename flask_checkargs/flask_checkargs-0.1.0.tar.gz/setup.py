try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='flask_checkargs',
    version='0.1.0',
    requires=['flask'],
    url='http://www.github.com/jsevilleja/flask_checkargs',
    include_package_data=True,
    license='MIT',
    author='Joel Sevilleja',
    author_email='joel@jsevilleja.org',
    description='A module to simplify checking arguments in Flask apps',
    packages = ["flask_checkargs"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
