#!/usr/bin/env python

from distutils.core import setup

setup(name='notify-me',
      version='0.9',
      description='Notify the user when a job is done or failed',
      author='Mohamed El-Kalioby',
      author_email='mkalioby@mkalioby.com',
      url='https://github.com/mkalioby/notify-me',
#      download_url="https://github.com/mkalioby/Python_Notifications/archive/0.1.tar.gz",
      packages=['notify_me'],
      keywords = ['admin','utils', 'notification'],
      data_files=[('/etc/',['notify_me/notify-me.cfg']),('/usr/local/bin/',['notify_me/notify-me'])]
     )
