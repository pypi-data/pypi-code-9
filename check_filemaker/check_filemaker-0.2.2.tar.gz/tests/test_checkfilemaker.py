# Copyright (C) 2015 Real Time Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from nose import with_setup
from nose.tools import raises
from check_filemaker import CheckFilemaker
import ConfigParser, os

class TestCheckFilemaker:
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('mytesting.cfg'))
        
        self.hostname = config.get('testing', 'hostname')
        self.username = config.get('testing', 'username')
        self.password = config.get('testing', 'password')
        
        self.databases = config.get('testing', 'databases').split(',')
        self.databases = [x.strip(' ') for x in self.databases]
        
        self.layout = config.get('testing', 'layout')
        
        self.fm = CheckFilemaker()
        self.fm.connect(self.hostname, self.username, self.password, self.databases[0], self.layout)
            
    def tearDown(self):
       pass
       
    def test_1(self):
        """Make sure we can find the database on the filemaker server"""
        
        mydb = [self.databases[0]]
        ret = self.fm.check_databases(mydb)
        assert(ret == set(mydb))
    
    def test_1_1(self):
        """Make sure we can find multiple database on the filemaker server"""
        
        mydb = self.databases
        ret = self.fm.check_databases(mydb)
        assert(ret == set(mydb))
                    
    def test_2(self):
        """Make sure we can do NOT find bad_db on the filemaker server"""

        # Umm, make sure you don't have a datbase called bad_db!
        #
        mydb = ['bad_db']
        ret = self.fm.check_databases(mydb)
        assert(ret == set([]))
    
    def test_2_1(self):
        """Make sure we catch when a database is not on the filemaker server"""
        
        mydb = self.databases
        ret = self.fm.check_databases(mydb)
        assert(ret == set(self.databases))
        
        mydb.append('baddb')
        assert(ret != set(mydb))

    @raises(Exception)    
    def test_3(self):
        """Test that bad hostname throws an exception"""
        
        fm2 = CheckFilemaker()
        fm2.connect('badhost.company.tld', self.username, self.password, self.database[0])

        mydb = [self.database[0]]
        ret = fm2.check_databases(mydb)
        
    @raises(Exception)    
    def test_4(self):
        """Test that bad username throws an exception"""
        
        fm2 = CheckFilemaker()
        fm2.connect(self.hostname, 'baduser', self.password, self.database[0])
        
        mydb = [self.database[0]]
        ret = fm2.check_databases(mydb)
        # I think PyFileMaker is buggy! Should get some sort of error/exception for bad user?
        #
        assert(False)
        

    @raises(Exception)    
    def test_5(self):
        """Test that bad password throws an exception"""
        
        fm2 = CheckFilemaker()
        fm2.connect(self.hostname, self.username, 'badpassword', self.database[0])

        mydb = [self.database[0]]
        ret = fm2.check_databases(mydb)
       
    def test_6(self):
        """Make sure we can find syssetting layout on the filemaker server"""

        # WARNING: layout names are case sensitive! sysSetting != syssetting
        layouts = [self.layout]
        ret = self.fm.check_layouts(layouts)
        assert(ret == set(layouts))
        
    def test_7(self):
        """Look for column named Constant with a value of 1"""

        # Might be specific to my testing Filemaker server
        #
        ret = self.fm.column(Constant='1')
        
        assert(len(ret) > 0)
        
    @raises(Exception)      
    def test_8(self):
        """Look for column named BadColumn with a value of 1"""

        ret = self.fm.column(BadColumn='1')

    def test_9(self):
        """Look for column named Constant with a value of 2"""

        ret = self.fm.column(Constant='2')
        assert(len(ret) == 0)
        assert(ret == [])