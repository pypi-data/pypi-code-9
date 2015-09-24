import os
from setuptools import find_packages
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# via https://github.com/larrycai/jenkins-buddy/blob/master/setup.py
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='jenkins-jobs-fail-the-build',
    version='1.0',
    author="Enrico Mills",
    author_email="enrico@nomadlabs.com",
    license="MIT",
    url="https://github.com/doubleo2/jenkins-jobs-fail-the-build",
    packages=find_packages(),
    long_description=(read('README.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    entry_points={
        'jenkins_jobs.builders': [
            'set-build-result=\
            jenkins_jobs_fail_the_build.builders:set_build_result']
    },
    install_requires=['jenkins-job-builder'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6', # Untested
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ]
    )
