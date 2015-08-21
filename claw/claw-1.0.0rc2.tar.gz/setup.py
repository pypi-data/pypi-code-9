import os

from setuptools import setup, find_packages


setup(
    name='claw',
    version='1.0.0rc2',
    description="Library to extract message quotations and signatures.",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    author='Adam Renberg',
    author_email='tgwizard@gmail.com',
    url='https://github.com/tgwizard/claw',
    license='APACHE2',
    packages=find_packages(exclude=['tests']),
    zip_safe=True,
    install_requires=[
        "lxml==2.3.3",
        "regex==0.1.20110315",
        "chardet==1.0.1",
        "dnspython==1.11.1",
        "html2text",
        "coverage",
        "flanker",
        "setuptools>=17.1",
    ],
    extras_require={
        'tests': [
            "nose==1.2.1",
            "mock",
        ],
        'dev': [
            'twine'
        ]
    },
)
