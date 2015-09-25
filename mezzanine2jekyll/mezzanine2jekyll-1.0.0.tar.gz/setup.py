from setuptools import find_packages, setup

from mezzanine2jekyll import __version__

setup(
    name='mezzanine2jekyll',
    version=__version__,
    license='BSD',
    author='Sam Kingston',
    author_email='sam@sjkwi.com.au',
    description='Django management command to add support for exporting Mezzanine\'s blog posts to Jekyll post files',
    long_description_markdown_filename='README.md',
    url='https://github.com/sjkingo/mezzanine2jekyll',
    install_requires=[
        'Mezzanine',
    ],
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
