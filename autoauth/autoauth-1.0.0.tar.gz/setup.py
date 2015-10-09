from setuptools import setup

setup(
    name='autoauth',
    py_modules=['autoauth'],
    version='1.0.0',
    author='David Keijser',
    author_email='keijser@gmail.com',
    description='authentication in urllib2 and requests for the command line',
    license='MIT',
    keywords='requests urllib2 authenticate',
    extras_require={'tests': ['PyHamcrest']}
)
