from setuptools import setup

setup(name='chessil_tourney_inserter',
      version='1.1',
      description='Uploads tournament data to Israel\'s chess federation site from SwissPerfect 98 generated SPDE files',
      url='http://github.com/unc0mm0n/ChessOrgIlTourneyInputer',
      author='Yuval Wyborski',
      author_email='yvw.bor@gmail.com',
      packages=['chessil_tourney_inserter'],
      zip_safe=False,
      entry_points={
      'console_scripts': [
            'insertchessiltourney = chessil_tourney_inserter.command_line:main']
      })