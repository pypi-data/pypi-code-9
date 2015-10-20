#encoding:utf-8
from setuptools import setup, find_packages
import sys, os

version = '1.2.3'

setup(name='qiniu4blog',
      version=version,
      description="写博客用的七牛图传",
      long_description="""写博客用的七牛图传""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python qiniu',
      author='wzyuliyang',
      author_email='wzyuliyang911@gmail.com',
      url='https://github.com/wzyuliyang/qiniu4blog',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'qiniu',
		'pyperclip',
      ],
      entry_points={
        'console_scripts':[
            'qiniu4blog = qiniu4blog.qiniu4blog:main'
        ]
      },
)
