from setuptools import setup

setup(name='jinja_wrapper',
      version='0.1',
      description='Wrapper for jinja',
      url='https://github.com/kevinslin',
      author='Kevin S Lin',
      author_email='kevinslin8@gmail.com',
      license='MIT',
      packages=['jinja_wrapper'],
      scripts = [
          'bin/jw.py'
          ],
      zip_safe=False)
