from setuptools import setup


setup(
    name="urlclustering",
    version="0.2",
    setup_requires=['setuptools-markdown'],
    author="Dimitris Giannitsaros",
    author_email="daremon@gmail.com",
    description="Facilitate clustering of similar URLs of a website",
    long_description_markdown_filename='README.md',
    license="MIT",
    keywords="cluster clustering urls",
    url="https://github.com/daremon/urlclustering",
    packages=['urlclustering'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
