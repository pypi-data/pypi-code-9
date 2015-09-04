from distutils.core import setup

setup(name='date_range',
    maintainer='Thomas Levine',
    maintainer_email='_@thomaslevine.com',
    description='Produce a sequence of dates. It\'s like the builtin range function but for datetime.date objects',
    url='https://github.com/tlevine/date_range.git',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    py_modules=['date_range'],
    version='0.0.1',
    license='LGPL'
)
