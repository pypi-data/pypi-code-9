from setuptools import setup

long_description = '''\
from wrap_amqp import Message

def cb(message):
    print message.body

Message(cb, <queue_name>, <consumer_tag>, <arguments_4_kombu.Connection>).loop()
'''

setup(
py_modules=['wrap_amqp'],
name='wrap_amqp',
version='1.0.4',
author='timchow',
author_email='jordan23nbastar@yeah.net',
license='LGPL',
install_requires=["amqp>=1.4.6", "kombu>=3.0.23"],
description='a wrapper for amqp',
keywords='amqp wrapper kombu',
url='http://tieba.baidu.com/f?ie=utf-8&kw=%E5%91%A8%E4%BA%95%E6%B1%9F',
long_description=long_description,
)
