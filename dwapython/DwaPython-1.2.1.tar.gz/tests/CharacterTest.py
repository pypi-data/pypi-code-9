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
__date__ ="$12.10.2014 4:08:10$"

import tests.DwaTestCase as DwaTestCase
import time

class CharacterTest(DwaTestCase.DwaTestCase):
  def setUp(self):
    DwaTestCase.DwaTestCase.setUp(self)
    self.character = self.d.character()
    self.user_data = self.d.user().token(self.credential)
    
    
    #we must create one to get data of it
    createParams = {}
    createParams['user_token'] = self.user_data['token']
    createParams['server_id'] = 1
    createParams['user_id'] = self.user_data['id']
    createParams['faction_id'] = 1
    createParams['name'] = 'UnitTestCharacter ' + str(time.time())
    createParams['class'] = 1
    createParams['x'] = 0
    createParams['y'] = 0
    createParams['z'] = 0
    createParams['rotation'] = 0
    createParams['gender'] = 1
    createParams['max_health']  = 200
    createParams['max_mana'] = 100
    self.createParams = createParams
    self.createData = self.character.create(createParams)

  def testList(self):
    listParams = {}
    listParams['server_id'] = 1
    #listParams['user_id'] = self.user_data['id']
    listParams['limit'] = 20
    listParams['page'] = 0

    
    listData = self.character.list(listParams)
    self.assertEqual(listData['message'], 'OK')
  
  def testSave(self):
    saveParams = {}
    saveParams['user_token'] = self.user_data['token']
    saveParams['user_id'] = self.user_data['id']
    saveParams['character_id'] = self.createData['id']
    saveParams['x'] = 10
    saveParams['y'] = 20
    saveParams['z'] = 30
    saveParams['health'] = 300
    saveParams['mana'] = 200
    saveParams['rotation'] = 0
    saveParams['reputation'] = 200
    saveParams['max_health'] = 500
    saveParams['max_mana'] = 1000
    saveParams['inventory'] = []

    
    saveData = self.character.save(saveParams)
    self.assertEqual(saveData['message'], 'Character saved')
    
  def testDetail(self):
    detailParams = {}
    detailParams['user_token'] = self.user_data['token']
    detailParams['user_id'] = self.user_data['id']
    detailParams['character_id'] = self.createData['id']

    
    detailData = self.character.detail(detailParams)
    self.assertEqual(detailData['message'], 'OK')
    
  def testCreate(self):
    createParams = {}
    createParams['user_token'] = self.user_data['token']
    createParams['server_id'] = 1
    createParams['user_id'] = self.user_data['id']
    createParams['faction_id'] = 1
    createParams['name'] = 'UnitTestCharacter ' + str(time.time())
    createParams['class'] = 1
    createParams['x'] = 0
    createParams['y'] = 0
    createParams['z'] = 0
    createParams['rotation'] = 0
    createParams['gender'] = 1
    createParams['max_health']  = 200
    createParams['max_mana'] = 100
    
    createData = self.character.create(createParams)
    
    self.assertEqual(createData['message'], 'Character created')
    self.assertIs(type(createData['id']), int)
  
  def testDelete(self):
    deleteParams = {}
    deleteParams['user_token'] = self.user_data['token']
    deleteParams['user_id'] = self.user_data['id']
    deleteParams['character_id'] = self.createData['id']
    
    createData = self.character.delete(deleteParams)
    
    self.assertEqual(createData['message'], 'Character deleted')

    