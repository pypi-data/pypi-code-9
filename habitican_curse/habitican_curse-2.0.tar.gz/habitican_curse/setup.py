from setuptools import setup

setup(
    name = 'habitican_curse',
    version = '1.2',
    scripts = ['habitican-curse', 'interface.py', 'helper.py', 'menu.py', 'debug.py', 'content.py', 'config.py', 'global_objects.py', 'screen.py', 'request_manager.py', 'task.py', 'user.py' ],
    url = 'https://github.com/rbavishi/Habitican-Curse',
    author = 'Rohan Bavishi',
    author_email = 'rohan.bavishi95@gmail.com',
    license = 'MIT',
    install_requires = [
      'requests'
    ]
)
