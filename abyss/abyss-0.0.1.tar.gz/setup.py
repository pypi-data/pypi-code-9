import os
from setuptools import setup, find_packages

# abyss
# MMO/RPG/RTS/RESTAPI game in your terminal!

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "abyss",
    version = "0.0.1",
    description = "MMO/RPG/RTS/RESTAPI game in your terminal!",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://www.bitbucket.org/johannestaas/abyss",
    packages=find_packages(),
    #package_dir={'abyss': 'abyss', },
    long_description=read('README.md'),
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
        'tinydb', 'pbkdf2'
    ],
    extras_require = {
        'server': ['flask'],
    },
    entry_points = {
        'console_scripts': [
            'abyss-server = abyss.server:main',
            'abyss = abyss:main',
        ],
    },
    #package_data = {
        #'abyss': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
