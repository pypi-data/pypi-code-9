"""
Programmer: JR Padfield
Description: Tool to help you save things in mysql
Version: 1
Date:
"""

import sqlalchemy

class mysql:
    """ Handles all mysql informtaion """

    def __init__(self, user, password, server, database):
        """ Creates the sqlalchemy engine with given paramerters """
        self.engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + server + '/' + database)
        self.conn = None

    def connect(self):
        """ Returns true if connection is open """
        try:
            self.conn = self.engine.connect()
            # its open so lets get to work.
            print("connection open")
            return True
        except:
            # didn't work so return false
            return False

    def close(self):
        """Returns true if connectin was closed """
        try:
            self.conn.close()
            print("connection closed")
        except:
            # didn't work oh snap
            print("error closing")
            return False

    def sendinfo(self, sql):
        """ Insert or edit data in the database, create database"""
        if self.connect():
            # connection opened lets execute a command
            self.conn.execute(sql)
            # lets close the connection.
            self.close()

    def pullinfo(self, sql):
        """ Pulls data from the database """
        if self.connect():
            # connection opened lets execute a command
            results = self.conn.execute(sql)
            # got the results of the sql. lets return it to  the user
            return results
