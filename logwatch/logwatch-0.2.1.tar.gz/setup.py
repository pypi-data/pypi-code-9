import os
from setuptools import setup

# logwatch
# Stupid small script to alert when a log is messing up - easier than setting up nagios right now

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "logwatch",
    version = "0.2.1",
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
    package_data = {
        'logwatch': ['.example_config.yml'],
    },
    include_package_data = True,
)

print('''
Configuration files' authority are in this order, from most important to least:
 * --config command line argument
 * ./.logwatch.{yml,yaml}
 * ~/.logwatch.{yml,yaml}
 * ~/.config/logwatch/config.{yml,yaml}
 * /etc/config/logwatch/config.{yml,yaml}

Variables from a less authoritative config will be used unless overridden
by a higher configuration, such as that passed by --config.

This means that if "sleep: 60" is defined in /etc/config/logwatch/config.yml,
it will be used unless another existing configuration defines "sleep: 30", and
so on.
''')
FINAL_CONFIG_PATH = '/etc/logwatch/example_config.yml'
EXAMPLE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'logwatch', '.example_config.yml')
if not os.path.exists(FINAL_CONFIG_PATH):
    try:
        import shutil
        os.makedirs(os.path.dirname(FINAL_CONFIG_PATH))
        shutil.copyfile(EXAMPLE_CONFIG_PATH, FINAL_CONFIG_PATH)
        print('Example configuration dropped to {}'.format(FINAL_CONFIG_PATH))
    except Exception:
        print('Please see documentation to see example configuration file.')
else:
    print('Please see example configuration at {}'.format(FINAL_CONFIG_PATH))
