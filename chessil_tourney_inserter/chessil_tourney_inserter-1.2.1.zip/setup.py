from setuptools import setup

setup(name='chessil_tourney_inserter',
      version='1.2.1',
      description='Uploads tournament data to Israel\'s chess federation site from SwissPerfect 98 generated SPDE files',
      url='http://github.com/unc0mm0n/chessil_tourney_inserter',
      author='Yuval Wyborski',
      author_email='yvw.bor@gmail.com',
      packages=['chessil_tourney_inserter'],
      zip_safe=False,

      install_requires = [
    'selenium'
    ],

      entry_points={
      'console_scripts': [
            'insertchessiltournament = chessil_tourney_inserter.command_line:main']
      })