from setuptools import setup

""" Create README.rst from README.md """
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='filmsontonight',
    version='0.1',
    description='Scrapes viewfilm.net to get the films on that night',
    long_description=read_md('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    url='http://github.com/jdbaldry/FilmsOnTonight',
    author='Jack Baldry',
    author_email='jdbaldry@gmail.com',
    license='MIT',
    packages=['filmsontonight'],
    install_requires=[
        'BeautifulSoup'
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'])
