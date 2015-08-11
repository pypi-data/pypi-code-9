from setuptools import setup

setup(name='asdb',
      version='0.2',
      description='Instant convenient debugger',
      url='https://github.com/alexmojaki/asdb',
      author='Alex Hall',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['asdb'],
      install_requires=['rpdb'],
      entry_points={
          'console_scripts': ['asdb=asdb.shell:main'],
      },
      zip_safe=False)
