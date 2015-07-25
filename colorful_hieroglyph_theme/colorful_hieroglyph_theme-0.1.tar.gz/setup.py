#from distutils.core import setup
from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    zip_safe=False,
    install_requires=[
        "sphinx>=1.1",
        "hieroglyph>=0.6",
        ],
    name="colorful_hieroglyph_theme",
    version=0.1,
    author="Lucy Wyman",
    author_email="lucyw@osuosl.org",
    description="A simple, colorful hieroglyph theme",
    long_description=long_description,
    packages=['colorful_hieroglyph_theme'],
    package_data={'colorful_hieroglyph_theme': ['colorful_hieroglyph_theme/static']},
    include_package_data=True,
    keywords="hieroglyph extension theme",
    url="https://github.com/lucywyman/colorful-hieroglyph-theme",
)

