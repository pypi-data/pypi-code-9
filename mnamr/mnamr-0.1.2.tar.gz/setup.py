from setuptools import setup, find_packages

setup(
    name="mnamr",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["imdbpie>=4.0.2"],
    entry_points={
        'console_scripts': [
            'mnamr = mnamr.mnamr:main',
        ],
    },
    author="Ali Kaafarani",
    author_email="ali@kvikshaug.no",
    description="Movie folder renamer",
    license="MIT",
    url="https://pypi.python.org/pypi/mnamr/",
)
