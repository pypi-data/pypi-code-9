from setuptools import setup

setup(name='fixalbumart',
      version='1.9',
      description='Automagically fix album arts of mp3 files, Even with incorrect tags!!!',
      url='https://github.com/yask123/fixalbumart/',
      author='Yask Srivastava',
      author_email='yask123@gmail.com',
      license='MIT',
      packages=['fixalbumart'],
      scripts=['bin/fixalbumart'],
      install_requires=[
          'eyed3',
      ],
      zip_safe=False)