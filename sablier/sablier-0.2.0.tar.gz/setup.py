from setuptools import setup


setup(
    name = 'sablier',
    version = '0.2.0',
    description = 'Python API to play with date, time and timezones',
    py_modules = ['sablier'],
    license = 'unlicense',
    author = 'Eugene Van den Bulke',
    author_email = 'eugene.vandenbulke@gmail.com',
    url = 'https://github.com/3kwa/sablier',
    install_requires = ['pytz'],
)
