from setuptools import setup

setup(name='trackmerge',
      version='0.3.0',
      description='Tool for tracking project release versions with git.',
      url='https://github.com/andrewguy9/trackmerge',
      author='andrew thomson',
      author_email='athomsonguy@gmail.com',
      install_requires = ['docopts>=0.6.1-fix2'],
      packages=['trackmerge'],
      scripts=['bin/ismerged', 'bin/isreleased'],
      zip_safe=False)
