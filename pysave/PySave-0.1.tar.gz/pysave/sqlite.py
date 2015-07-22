"""
Programmer: JR Padfield
Description: Tool to help you save things in sqlite
Version: 1
Date:
"""

import sqlite3
import os

class sqlite:

    def __init__(self, database):
        self.database = database
        self.sqlite = sqlite3.connect(self.database)

    def openconnection(self):
        """ Opens up a connection and returns true if successful """
        try:
            self.sqlite = sqlite3.Connection(self.database)
            print("Connection is open")
            return True
        except sqlite3.Error as e:
            print(e)
            return False

    def closeconnection(self,):
        """ Closes the database connection """
        self.sqlite.close()
        print("Connection is closed")

    def createdatabase(self, dbname):
        """ Creates the database """
        if not os.path.isfile(dbname + ".sqlite"):
            self.sqlite = sqlite3.connect(dbname + ".sqlite")
        else:
            print("Database: " + dbname + " already exsits")

    def sqlcommand(self, command):
        """ Executes the given command """
        if self.openconnection():
            self.sqlite.cursor().execute(command)
            self.sqlite.commit()
            self.closeconnection()
            print("SqlCommand executed good")
