from setuptools import setup

setup(name='weaver',
      version='0.1',
      description='Wrapper for Fabric',
      url='',
      author='Kevin Lin',
      author_email='kevinslin8@gmail.com',
      license='MIT',
      packages=['weaver', 'weaver.topic', 'weaver.contrib',
      'weaver.contrib.noah'],
      zip_safe=False)
