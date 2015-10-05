# Copyright (C) 2014 Adam Schubert <adam.schubert@sg1-game.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__="Adam Schubert <adam.schubert@sg1-game.net>"
__date__ ="$12.10.2014 2:28:12$"


import unittest
import dwa
import os
import time

class DwaTestCase(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    conf_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_token.conf'))
    api_key = conf_file.read().strip()
    conf_file.close()
    self.d = dwa.Dwa(api_key, 'http://apitest.divine-warfare.com/')
    self.credential = {'password': api_key, 'username': 'unittest-' + api_key + str(time.time())}
    
    #always create user
    params = {}
    params['password'] = self.credential['password']
    params['username'] = self.credential['username']
    params['nickname'] = generateNickname()
    params['email'] = self.credential['username'] + '@divine-warfare.com'
    params['active'] = True
    self.d.user().create(params)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    #always destroy user
    userData = self.d.user().token({'password': self.credential['password'], 'username': self.credential['username']})
    delParams = {}
    delParams['user_id'] = userData['id']
    delParams['user_token'] = userData['token']
    self.d.user().delete(delParams)
    
    
def generateNickname():
  ret = []
  for num in str(time.time()).replace('.', ''):
    ret.append(chr(int(num) + ord('a')))
    
  return "".join(ret)
    
        


