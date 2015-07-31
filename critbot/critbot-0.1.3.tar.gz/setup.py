from distutils.core import setup

setup(
    name='critbot',
    version='0.1.3',
    description='Sending critical errors to syslog, slack, email, {your_plugin}.',
    long_description='''
Install::

    pip install critbot

Add to "config.py" file::

    import critbot.plugins.syslog
    import critbot.plugins.slack
    import critbot.plugins.email
    from critbot import crit_defaults

    crit_defaults.subject = 'MyService host:port CRIT'

    crit_defaults.plugins = [
        critbot.plugins.syslog.plugin(),
        critbot.plugins.slack.plugin(
            token='Get it from https://my.slack.com/services/new/bot',
            channel='#general', # '@private' or '#channel'
            users='', # '@user1 @user2 @userN'
        ),
        critbot.plugins.email.plugin(
            to='Name1 <user1@example.com>, Name2 <user2@example.com>',
            user='critbot@example.com', # Add more config if not GMail.
            password='pa$$word',
        ),
    ]

Check other config options and their defaults, e.g. "seconds_per_notification=60":

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/core.py#L23 - "crit_defaults"

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/syslog.py#L17

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/slack.py#L14

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/email.py#L14

Use "crit" in other files of your project::

    from critbot import crit

    try:
        1/0
    except Exception:
        crit()
        # More processing if needed.

    try:
        1/0
    except Exception:
        crit(also='test2')

    if True:
        crit('test3')

Please fork https://github.com/denis-ryzhkov/critbot
and create pull requests with new plugins inside.

''',
    url='https://github.com/denis-ryzhkov/critbot',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'critbot',
        'critbot.plugins',
    ],
    install_requires=[
        'adict',
        'requests',
        'send_email_message',
    ],
)
