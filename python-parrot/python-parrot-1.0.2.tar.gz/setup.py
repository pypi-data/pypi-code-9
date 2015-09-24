from setuptools import find_packages, setup

from parrot import __version__

setup(
    name='python-parrot',
    version=__version__,
    license='BSD',
    author='Sam Kingston',
    author_email='sam@sjkwi.com.au',
    description='Parrot is a simple HTTP server that responds to requests with a specified filename',
    long_description_markdown_filename='README.md',
    url='https://github.com/sjkingo/python-parrot',
    #setup_requires=[
    #    'setuptools-markdown',
    #],
    install_requires=[
        'python-magic',
    ],
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points="""
        [console_scripts]
        parrot=parrot.parrot:main
    """,
)
