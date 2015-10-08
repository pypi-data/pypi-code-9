#encoding:utf-8
from setuptools import setup, find_packages
import sys, os

version = '1.1.2'

setup(name='byrlogin',
      version=version,
      description="北邮人登录网关脚本",
      long_description="""北邮人登录网关脚本""",
      classifiers=[],
      keywords='python byrlogin',
      author='wzyuliyang',
      author_email='wzyuliyang911@gmail.com',
      url='https://github.com/wzyuliyang/byrlogin',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
        'prompt_toolkit',
      ],
      entry_points={
        'console_scripts':[
            'byrlogin = byrlogin.byrlogin:main'
        ]
      },
)
