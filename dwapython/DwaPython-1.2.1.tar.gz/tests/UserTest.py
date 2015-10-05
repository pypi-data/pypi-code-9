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
__date__ ="$12.10.2014 2:20:45$"

import tests.DwaTestCase as DwaTestCase
import unittest
import time

class UserTest(DwaTestCase.DwaTestCase):
  def setUp(self):
    DwaTestCase.DwaTestCase.setUp(self)
    self.user = self.d.user()
    self.username = self.credential['username'] + 'UserTest' + str(time.time())
  
  def testCreate(self):
    params = {}
    params['password'] = self.credential['password']
    params['username'] = self.username
    params['nickname'] = DwaTestCase.generateNickname()
    params['email'] = self.username + '@divine-warfare.com'
    params['active'] = True
    #create
    message = self.user.create(params)['message']
    
    #delete
    userData = self.user.token({'password': params['password'], 'username': params['username']})
    
    delParams = {}
    delParams['user_id'] = userData['id']
    delParams['user_token'] = userData['token']
    self.user.delete(delParams)
    
    self.assertEqual(message, 'User created')
    
  def testDelete(self):
    params = {}
    params['password'] = self.credential['password']
    params['username'] = self.username
    params['nickname'] = DwaTestCase.generateNickname()
    params['email'] = self.username + '@divine-warfare.com'
    params['active'] = True
    
    #create
    self.user.create(params)
    userData = self.user.token({'password': params['password'], 'username': params['username']})
    
    delParams = {}
    delParams['user_id'] = userData['id']
    delParams['user_token'] = userData['token']
    #delete
    message = self.user.delete(delParams)['message']
    self.assertEqual(message, 'User deleted')
    
  def testList(self):
    data = self.user.list({'limit': 20, 'page': 0})
    self.assertEqual(data['message'], 'OK')
    self.assertIsNotNone(data['data'])
    self.assertIsNotNone(data['pages'])
    
  def testToken(self):
    data = self.user.token(self.credential)
    self.assertEqual(data['message'], 'Token created')
    self.assertEqual(len(data['token']), 32)
    self.assertIsNotNone(data['id'])
    self.assertRegexpMatches(data['token_expiration'], '(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
    
  def testPassword(self):
    data_token = self.user.token(self.credential)
    data = self.user.password({'old_password': self.credential['password'], 'new_password': self.credential['password'], 'user_token': data_token['token'], 'user_id': data_token['id']})
    self.assertEqual(data['message'], 'Password changed')
    
  def testActive(self):
    data_token = self.user.token(self.credential)
    data = self.user.active({'user_id': data_token['id'], 'active': True, 'user_token': data_token['token']})
    self.assertEqual(data['message'], 'User activated')
    
  def testDeactive(self):
    data_token = self.user.token(self.credential)
    data = self.user.active({'user_id': data_token['id'], 'active': False, 'user_token': data_token['token']})
    self.assertEqual(data['message'], 'User deactivated')

  #Will fail cos our mailserver checks if maildir exists...
  #@unittest.expectedFailure    
  def testRequestPasswordReset(self):
    email = self.credential['username'] + '@example.com';
    
    content_fill = 'abc' * 5333 #16k of shit
    
    data = self.user.request_password_reset({'email': email, 'email_content': 'URL: example.com/password/reset/{reset_token}' + content_fill, 'email_subject': 'Password reset unittest', 'email_from': 'unittest@example.com'})
    #self.assertEqual(data['message'], 'Email with reset token has been send')
    self.assertEqual(data['message'], 'Email not found')
    
  @unittest.expectedFailure
  def testDoPasswordReset(self):
    #we use USER token as password reset token, cos we dont have reset token (and we cant have it cos it is only in email) so this call will fail, and that is a good thing :)
    data_token = self.user.token(self.credential)
    data = self.user.request_password_reset({'reset_token': data_token['token'], 'new_password': 'newPassword'})
    self.assertEqual(data['message'], 'Password changed')
