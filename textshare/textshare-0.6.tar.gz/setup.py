from setuptools import setup

setup(name='textshare',
      version='0.6',
      description='share your text files easily',
      url='https://github.com/bindingofisaac/textshare',
      author='Vivek',
      author_email='bindingofisaacs@gmail.com',
      license='MIT',
      packages=['textshare'],
      entry_points={
          'console_scripts': ['textshare=textshare.command_line:cli'],
      },
      install_requires=[
          'click',
          'requests'
      ],
      zip_safe=False)
