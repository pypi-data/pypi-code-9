#!/usr/bin/python2
# -*- coding: utf-8 -*-

# ==============================================================================
#      Frank Matranga's Third-party Regis High School Python Module
# ==============================================================================

import sys
import os
from scraper import Scraper
from cli import CLI
from viewer import Viewer
import json
from pymongo import MongoClient
import requests
from lxml import html

PATH = "./secrets.json"

IP = "localhost" if len(sys.argv) < 3 else sys.argv[2]
PORT = "27017" if len(sys.argv) < 4 else sys.argv[3]
DB_NAME = "regis" if len(sys.argv) < 5 else sys.argv[4]

class TRP:
    def __init__(self, path=PATH, ip=IP, port=PORT, db_name=DB_NAME):
        self.path = path
        self.ip = ip
        self.port = port
        self.db_name = db_name

        print ip
        print " --- Initalizing TRP Module ---\n"
        #print "Arguments: "+str(sys.argv[1::])
        self.secrets = self.get_secrets()
        self.username = self.secrets['regis_username']
        self.password = self.secrets['regis_password']
        print "Found info for Regis student '"+self.username+"'"
        self.connect_to_db()
        self.session = self.get_session()
        self.init_mods()
        print "\n --- READY --- \n"

    def get_secrets(self):
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            self.path = sys.argv[1]

        if os.path.isdir(self.path):
            if self.path[-1] != "/":
                self.path += "/"
            self.path += "secrets.json"


        try:
            secrets = json.loads(open(self.path).read())
        except (ValueError, IOError):
            print "'"+self.path+"' is not a valid secrets.json"
            self.exit()

        print "Using path '"+self.path+"' for secrets.json"
        return secrets

    def connect_to_db(self):
        try:
            print "Attempting to connect to mongodb://"+self.ip+":"+self.port+"/"+self.db_name+"..."
            self.client = MongoClient('mongodb://'+self.ip+':'+self.port+'/')
            self.db = self.client[DB_NAME]
            self.db.authenticate('ontrac', 'ontrac')
            self.db.students.count()
            print "Done."
        except Exception: # nasty I know
            self.client = None
            print "Failed to connect to Database."
            self.exit()

    def get_session(self):
        print "Attempting logins..."
        url = "https://moodle.regis.org/login/index.php"
        values = {'username': self.username, 'password': self.password}
        session = requests.Session()
        r = session.post(url, data=values)
        parsed_body = html.fromstring(r.text)
        title = parsed_body.xpath('//title/text()')[0]

        # Check whether login was successful or not
        if not "My home" in title:
            print "Failed to login to Moodle, check your credentials."
            self.exit()
        print "Logged into Moodle."

        url = "https://intranet.regis.org/login/submit.cfm"
        values = {'username': self.username, 'password': self.password, 'loginsubmit': ''}
        r = session.post(url, data=values)
        parsed_body = html.fromstring(r.text)
        try:
            title = parsed_body.xpath('//title/text()')[0]
            if not "Intranet" in title:
                print "Failed to login to the Intranet, check your credentials."
                quit()
        except:
            print "Failed to login to the Intranet, check your credentials."
            quit()

        print "Logged in to the Intranet."
        print "Done."
        return session

    def init_mods(self):
        print "Initialzing modules..."
        self.viewer = Viewer(self.db)
        self.scraper = Scraper(self.db, self.session)
        self.cli = CLI(self.db)
        print "Done."

    def exit(self):
        try: # this might be run before it is assigned
            self.client.close()
            print "Closed DB connection."
        except:
            pass

        print "Shutting down..."
        quit()
        sys.exit()

def main():
    t = TRP()
    t.exit()

if __name__ == "__main__":
    main()
