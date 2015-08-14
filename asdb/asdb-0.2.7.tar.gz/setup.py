from setuptools import setup

setup(name='asdb',
      version='0.2.7',
      description='Instant convenient debugger',
      url='https://github.com/alexmojaki/asdb',
      author='Alex Hall',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['asdb'],
      install_requires=['rpdb'],
      scripts=['bin/asdb'],
      zip_safe=False)
