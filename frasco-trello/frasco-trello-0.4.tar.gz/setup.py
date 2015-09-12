from setuptools import setup, find_packages


setup(
    name='frasco-trello',
    version='0.4',
    url='http://github.com/frascoweb/frasco-trello',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Trello integration for Frasco",
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'frasco-users',
        'python-dateutil==2.4.0',
        'requests_oauthlib'
    ]
)
