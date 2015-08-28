import os
from setuptools import setup

# logwatch
# Stupid small script to alert when a log is messing up - easier than setting up nagios right now

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "logwatch",
    version = "0.1.0",
    description = "Email alerts when tail -1 of log file does not match regex",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://www.bitbucket.org/johannestaas/logwatch",
    packages=['logwatch'],
    package_dir={'logwatch': 'logwatch'},
    long_description=read('README.rst'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'yamlcfg', 
    ],
    entry_points = {
        'console_scripts': [
            'logwatch = logwatch.watcher:main',
        ],
    },
    #package_data = {
        #'logwatch': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
