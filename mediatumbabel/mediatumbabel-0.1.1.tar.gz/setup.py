from setuptools import setup
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="mediatumbabel",
    version=find_version('mediatumbabel', '__init__.py'),
    description="flask-babel port to provide i18n for mediaTUM (+jinja2) with some improvements",
    # The project URL.
    url='https://mediatumdev.ub.tum.de/projects/mediatum-babel',
    # Author details
    author='Tobias Stenzel',
    author_email='tobias.stenzel@tum.de',
    # Choose your license
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database'
    ],
    keywords='babel i18n pybabel mediatum',
    packages=["mediatumbabel"],
    install_requires=["babel"],
    include_package_data=True,
)
