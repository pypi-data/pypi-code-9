import setuptools

setuptools.setup(
    name='tractdb',
    version='0.1.1',
    description='TractDB',
    url='https://tractdb.org',
    packages=['tractdb'],
    install_requires=[
        'couchdb',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': ['tractdb_admin=tractdb.admin_cmd:main'],
    },
    zip_safe=False,
)
