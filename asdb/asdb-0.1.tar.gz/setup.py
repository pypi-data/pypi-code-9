from setuptools import setup

setup(name='asdb',
      version='0.1',
      description='Instant convenient debugger',
      url='https://github.com/alexmojaki/asdb',
      author='Alex Hall',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['asdb'],
      requirements=['rpdb', 'IPython'],
      zip_safe=False)
