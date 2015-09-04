import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

ns = {}
with open(os.path.join(here, 'kyper-util', 'version.py')) as f:
   exec(f.read(), {}, ns)

setup(
   name='kyper.util',
   version=ns['__version__'],
   author='Kyper Developers',
   author_email='developers@kyperdata.com',
   packages=find_packages(),
   url='https://git.kyper.co/kyper/kyper-util',
   description='Kyper Utilities',
   install_requires=[
      "kyper",
      "Flask",
      "parse",
      "numpy",
      "pandas",
      "pytz",
      "requests",
      "boto",
      "future==0.14.3"
   ]
)
