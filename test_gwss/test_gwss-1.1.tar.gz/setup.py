from setuptools import setup

setup(name='test_gwss',
      version='1.1',
      description='Garena gas stats system',
      url='http://github.com/storborg/funniest',
      author='Tran Minh Tri',
      author_email='tranmt@garena.com',
      license='MIT',
      packages=['test_gwss'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)