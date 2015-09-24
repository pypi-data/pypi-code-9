import ez_setup
ez_setup.use_setuptools()

from setuptools import setup,find_packages

setup(
    name = "gcal2gcal",
    version = "1.0.1",
    author = "Grentius",
    author_email = "grentius@mailmight.com",
    description = "Package to upload GroupCalendar events to Google Calendar",
    license = "BSD",
    url = "http://code.google.com/p/gcal2gcal/",
    install_requires=['gdata>=1.0.2','setuptools>=0.6c12'],
    package_dir={'gcal2gcal':'src'},
    packages=['gcal2gcal'],
    entry_points = {
        'console_scripts': ['gcal2gcal = gcal2gcal.gcal2gcal:main']
        }
    )
