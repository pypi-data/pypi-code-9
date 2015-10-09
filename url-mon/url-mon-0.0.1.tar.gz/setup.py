__author__ = 'jiasir'
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("url-mon now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

setup(name='url-mon',
      version='0.0.1',
      description='URL Monitor',
      author='jiasir',
      author_email='jiasir@icloud.com',
      url='https://github.com/jiasir/url-mon/',
      license='MIT License',
      install_requires=[],
      packages=find_packages(),
      scripts=[
          'url-mon.py',
      ],
      data_files=[],)
