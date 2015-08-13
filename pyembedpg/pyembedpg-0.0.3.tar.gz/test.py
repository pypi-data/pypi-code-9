from pyembedpg import PyEmbedPg

with PyEmbedPg('9.4.0').start([15432, 15433, 15434, 15436]) as pg:
  pg.create_user('scott', 'tiger') # create a user scott with password tiger
  pg.create_database('testdb', 'scott') # create database testdb with owner       scott - See more at: http://www.simulmedia.com/resources/blog/pyembedpg-simple-way-use-postgres-python-integration-tests/#sthash.0AiTgZZu.dpuf
  print pg.running_port
  raise Exception('t')
  pass

