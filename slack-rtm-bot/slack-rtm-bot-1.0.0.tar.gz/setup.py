from setuptools import setup

with open('README.md', 'r') as f:
  readme = f.read()

setup(
    name='slack-rtm-bot',
    version='1.0.0',
    description='Slack RTM bot',
    long_description=readme,
    url='https://github.com/nkouevda/slack-rtm-bot',
    author='Nikita Kouevda',
    author_email='nkouevda@gmail.com',
    license='MIT',
    packages=[
        'slack_rtm_bot',
        'slack_rtm_bot.handlers',
    ],
    install_requires=[
        'requests',
        'six',
        'slackclient',
        'websocket-client',
    ],
    entry_points={
        'console_scripts': [
            'slack-rtm-bot=slack_rtm_bot.bot:main',
        ],
    },
)
