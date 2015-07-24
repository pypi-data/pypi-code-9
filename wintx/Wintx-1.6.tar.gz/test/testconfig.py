#!/usr/bin/env python
import collections
import ConfigParser
import os

TESTCONFFILE = './test.conf'

class TestConfig(collections.MutableMapping):
  def __init__(self):
    super(TestConfig, self).__init__()

    testconf_file = os.path.abspath('./test.conf')
    if( not os.path.exists(testconf_file) ):
      raise Exception('Unable to locate the testing config file. '\
          'Looking at %s.' % testconf_file)
    
    testconf_parser = ConfigParser.ConfigParser()
    files_read = testconf_parser.read([testconf_file])
    if( not files_read ):
      raise Exception('Unable to read file %s.' % testconf_file)

    self.settings = {}
    for section in testconf_parser.sections():
      self.settings[section] = {}
      for option in testconf_parser.options(section):
        self.settings[section][option] = testconf_parser.get(section,option)

  def __setitem__(self, key, value):
    self.settings[key] = value

  def __getitem__(self, key):
    return self.settings[key]

  def __delitem__(self, key):
    del self.settings[key]

  def __iter__(self):
    return iter(self.settings)

  def __len__(self):
    return len(self.settings)

  def keys(self):
    return self.settings.keys()

  def values(self):
    return [self[key] for key in self]

  def itervalues(self):
    return (self[key] for key in self)
