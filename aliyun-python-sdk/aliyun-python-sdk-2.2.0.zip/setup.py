__author__ = 'yudan.lyd'

from distutils.core import setup

setup(
    name='aliyun-python-sdk',
    version='2.2.0',
    author='Septimus',
    author_email='yudan.lyd@alibaba-inc.com',
    packages=['aliyun', 'aliyun.api', 'aliyun.api.rest',
              'aliyun.api.rest.bss',
              'aliyun.api.rest.cdn',
              'aliyun.api.rest.dns',
              'aliyun.api.rest.ecs',
              'aliyun.api.rest.ess',
              'aliyun.api.rest.mkvstore',
              'aliyun.api.rest.mts',
              'aliyun.api.rest.ocm',
              'aliyun.api.rest.ocs',
              'aliyun.api.rest.odps',
              'aliyun.api.rest.push',
              'aliyun.api.rest.ram',
              'aliyun.api.rest.rds',
              'aliyun.api.rest.rkvstore',
              'aliyun.api.rest.slb'],
    include_package_data=True,
    scripts=[],
    description='All modules of aliyun python sdk.',
    install_requires=[]
)
